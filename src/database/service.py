"""Lifecycle management for the local PocketBase child process."""
from __future__ import annotations

import asyncio
import os
import secrets
import shutil
import socket
import subprocess
import sys
from pathlib import Path

from .client import PocketBaseClient
from .constants import _SCHEMA_MIGRATION, MIGRATION_NAME, SUPERUSER_EMAIL
from .errors import PocketBaseError


def _find_original_executable() -> Path | None:
    """Returns the true executable path without pulling in GUI widgets."""
    try:
        import __compiled__
        orig = getattr(__compiled__, "original_argv0", None)
        if orig and Path(orig).exists():
            return Path(orig).resolve()
    except (ImportError, OSError, TypeError):
        pass
    if appimage := os.environ.get("APPIMAGE"):
        if Path(appimage).exists():
            return Path(appimage).resolve()
    if sys.argv and Path(sys.argv[0]).exists():
        return Path(sys.argv[0]).resolve()
    return None


class PocketBaseService:
    """Owns the bundled PocketBase child process and its authenticated client."""

    def __init__(self, data_directory: str | Path, binary_path: str | Path | None = None):
        self.data_directory = Path(data_directory).expanduser().resolve()
        self.binary_path = Path(binary_path).expanduser().resolve() if binary_path else None
        self.migrations_directory = self.data_directory / "_porn_fetch_migrations"
        self.process: subprocess.Popen[bytes] | None = None
        self.client: PocketBaseClient | None = None

    def find_binary(self, custom_path: str | Path | None = None) -> Path:
        target_path = custom_path or self.binary_path
        if target_path:
            p = Path(target_path).expanduser()
            if p.is_file() and (sys.platform == "win32" or os.access(p, os.X_OK)):
                return p.resolve()
        name = "pocketbase.exe" if sys.platform == "win32" else "pocketbase"
        candidates: list[Path] = []
        if configured := os.environ.get("PORN_FETCH_POCKETBASE_BINARY"):
            candidates.append(Path(configured).expanduser())
        orig = _find_original_executable()
        if orig is not None:
            candidates.append(orig.parent / name)
        project_root = Path(__file__).resolve().parents[2]
        candidates.extend([
            project_root / name,
            project_root / "packaging" / "pocketbase" / name,
            project_root / "packaging" / "pocketbase" / sys.platform / name,
        ])
        if installed := shutil.which("pocketbase"):
            candidates.append(Path(installed))
        for candidate in candidates:
            if candidate.is_file() and (sys.platform == "win32" or os.access(candidate, os.X_OK)):
                return candidate.resolve()
        searched = ", ".join(str(path) for path in candidates)
        raise PocketBaseError(
            "PocketBase tracking is enabled, but the PocketBase binary was not found. "
            "Place it beside the Porn Fetch executable, install it on PATH, or set "
            f"PORN_FETCH_POCKETBASE_BINARY. Searched: {searched}"
        )

    async def start(self) -> PocketBaseClient:
        if self.client is not None:
            return self.client
        if self.data_directory.exists() and not self.data_directory.is_dir():
            raise PocketBaseError(f"PocketBase data path is not a directory: {self.data_directory}")
        self.migrations_directory.mkdir(parents=True, exist_ok=True)
        migration_path = self.migrations_directory / MIGRATION_NAME
        await asyncio.to_thread(migration_path.write_text, _SCHEMA_MIGRATION, "utf-8")

        binary = self.find_binary()
        password = secrets.token_urlsafe(32)
        flags = [
            f"--dir={self.data_directory}",
            f"--migrationsDir={self.migrations_directory}",
        ]
        await self._run_command(
            binary, "superuser", "upsert", SUPERUSER_EMAIL, password, *flags
        )

        port = self._reserve_port()
        self.process = await asyncio.to_thread(
            self._spawn_server,
            binary,
            port,
            flags,
        )
        client = PocketBaseClient(f"http://127.0.0.1:{port}")
        try:
            await self._wait_until_healthy(client)
            await client.authenticate(SUPERUSER_EMAIL, password)
        except Exception:
            await self.stop()
            raise
        self.client = client
        return client

    async def _run_command(self, binary: Path, *arguments: str) -> None:
        creation_flags = subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
        try:
            result = await asyncio.to_thread(
                subprocess.run,
                [str(binary), *arguments],
                cwd=str(binary.parent),
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                timeout=15,
                check=False,
                creationflags=creation_flags,
            )
        except subprocess.TimeoutExpired:
            raise PocketBaseError(f"PocketBase command timed out: {' '.join(arguments[:2])}")
        if result.returncode:
            details = result.stdout.decode("utf-8", errors="replace").strip()
            raise PocketBaseError(
                f"PocketBase command failed ({' '.join(arguments[:2])}): {details}"
            )

    @staticmethod
    def _spawn_server(binary: Path, port: int, flags: list[str]) -> subprocess.Popen[bytes]:
        creation_flags = subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
        return subprocess.Popen(
            [str(binary), "serve", f"--http=127.0.0.1:{port}", "--automigrate=false", *flags],
            cwd=str(binary.parent),
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=creation_flags,
        )

    @staticmethod
    def _reserve_port() -> int:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener:
            listener.bind(("127.0.0.1", 0))
            return int(listener.getsockname()[1])

    async def _wait_until_healthy(self, client: PocketBaseClient) -> None:
        for _ in range(50):
            if self.process is not None and self.process.poll() is not None:
                raise PocketBaseError(
                    f"PocketBase exited during startup with code {self.process.returncode}"
                )
            try:
                await client.request("GET", "/api/health", authenticated=False)
                return
            except PocketBaseError:
                await asyncio.sleep(0.1)
        raise PocketBaseError("PocketBase did not become healthy within 5 seconds")

    async def stop(self) -> None:
        self.client = None
        process, self.process = self.process, None
        if process is None or process.poll() is not None:
            return
        process.terminate()
        try:
            await asyncio.to_thread(process.wait, 5)
        except subprocess.TimeoutExpired:
            process.kill()
            await asyncio.to_thread(process.wait)
