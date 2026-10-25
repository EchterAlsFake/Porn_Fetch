"""Application-owned Tor client. No relay, system service or media proxy changes."""
from __future__ import annotations

import atexit
import json
import os
import re
import socket
import subprocess
import sys
import threading
import time
from pathlib import Path

from .paths import shared_data_dir


class TorUnavailable(ConnectionError):
    """Tor could not become ready; callers must not retry outside Tor."""


def bundled_binary() -> Path:
    override = os.environ.get("PORNFETCH_TOR_BINARY")
    if override and not getattr(sys, "frozen", False):
        return Path(override).expanduser().resolve()
    if hasattr(sys, "getandroidapilevel") or os.environ.get("ANDROID_ARGUMENT"):
        # Qt's Android native-library directory is supplied by the GUI adapter.
        directory = os.environ.get("PORNFETCH_ANDROID_NATIVE_LIB_DIR")
        if directory:
            return Path(directory) / "libTor.so"
        try:
            info = json.loads((Path(os.environ["ANDROID_PRIVATE"]) / "pornfetch-platform.json").read_text())
            return Path(info["nativeLibraryDir"]) / "libTor.so"
        except (OSError, KeyError, ValueError):
            raise TorUnavailable("Android Tor platform configuration is unavailable") from None
    name = "tor.exe" if sys.platform == "win32" else "tor"
    roots = [Path(__file__).with_name("tor"), Path(sys.executable).parent / "src/shared/tor"]
    if getattr(sys, "_MEIPASS", None):
        roots.insert(0, Path(sys._MEIPASS) / "src/shared/tor")
    return next((root / name for root in roots if (root / name).is_file()), roots[0] / name)


class TorRuntime:
    def __init__(self, *, binary=None, directory=None, bootstrap_timeout=180, progress=None):
        self.binary = binary
        self.directory = directory
        self.bootstrap_timeout = bootstrap_timeout
        self.progress = progress or (lambda _state, _percent: None)
        self.process = None
        self.proxy = None
        self.state = "stopped"
        self.percent = 0
        self._lock = threading.Lock()
        self._stopped = threading.Event()

    def _report(self, state, percent=0):
        self.state, self.percent = state, percent
        try:
            self.progress(state, percent)
        except RuntimeError:
            # Qt may already have destroyed the presentation adapter at exit.
            pass

    def _control(self, directory):
        line = (directory / "control-port").read_text().strip()
        match = re.fullmatch(r"PORT=127\.0\.0\.1:(\d+)", line)
        if not match:
            raise TorUnavailable("Invalid local Tor control endpoint")
        cookie = (directory / "control_auth_cookie").read_bytes()
        if len(cookie) != 32:
            raise TorUnavailable("Invalid Tor control cookie")
        with socket.create_connection(("127.0.0.1", int(match[1])), timeout=2) as connection:
            connection.sendall(b"AUTHENTICATE " + cookie.hex().encode() + b"\r\nGETINFO status/bootstrap-phase net/listeners/socks\r\nQUIT\r\n")
            data = b""
            while len(data) < 65536:
                chunk = connection.recv(4096)
                if not chunk:
                    break
                data += chunk
        if not data.startswith(b"250 OK") or b"250-status/bootstrap-phase=" not in data:
            raise TorUnavailable("Tor control authentication failed")
        return data.decode("ascii", errors="replace")

    def ensure_ready(self):
        with self._lock:
            if self.process is not None and self.process.poll() is None and self.proxy:
                return self.proxy
            self.stop()
            self._stopped.clear()
            binary = Path(self.binary or bundled_binary())
            if not binary.is_file():
                self._report("error")
                raise TorUnavailable("Bundled Tor is unavailable for this build")
            private = Path(os.environ["ANDROID_PRIVATE"]) if "ANDROID_PRIVATE" in os.environ else shared_data_dir()
            directory = Path(self.directory or private / "tor-client")
            directory.mkdir(parents=True, exist_ok=True, mode=0o700)
            if os.name != "nt":
                directory.chmod(0o700)
            (directory / "control-port").unlink(missing_ok=True)
            (directory / "torrc").write_text("# Managed by Porn Fetch.\n", encoding="ascii")
            self._report("connecting")
            try:
                environment = os.environ.copy()
                if sys.platform.startswith("linux") or hasattr(sys, "getandroidapilevel"):
                    environment["LD_LIBRARY_PATH"] = str(binary.parent)
                elif sys.platform == "darwin":
                    environment["DYLD_LIBRARY_PATH"] = str(binary.parent)
                self.process = subprocess.Popen(
                    [str(binary), "-f", str(directory / "torrc"), "--DataDirectory", str(directory), "--SocksPort", "127.0.0.1:auto",
                     "--ControlPort", "127.0.0.1:auto", "--ControlPortWriteToFile", str(directory / "control-port"),
                     "--CookieAuthentication", "1", "--ClientOnly", "1", "--AvoidDiskWrites", "1",
                     "--SafeLogging", "1", "--Log", "err stderr"],
                    cwd=str(binary.parent), stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL, creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
                    env=environment,
                )
                deadline = time.monotonic() + self.bootstrap_timeout
                while not self._stopped.is_set() and time.monotonic() < deadline:
                    if self.process is None or self.process.poll() is not None:
                        raise TorUnavailable("Tor stopped before connecting")
                    try:
                        reply = self._control(directory)
                        percentage = re.search(r"\bPROGRESS=(\d+)", reply)
                        self._report("connecting", int(percentage[1]) if percentage else 0)
                        endpoint = re.search(r'net/listeners/socks="127\.0\.0\.1:(\d+)"', reply)
                        if self.percent == 100 and endpoint:
                            self.proxy = f"socks5h://127.0.0.1:{endpoint[1]}"
                            self._report("ready", 100)
                            return self.proxy
                    except (OSError, TorUnavailable):
                        pass
                    self._stopped.wait(0.25)
                raise TorUnavailable("Tor did not connect; no direct connection was attempted")
            except BaseException:
                self.stop()
                self._report("error")
                raise

    def stop(self):
        self._stopped.set()
        process, self.process = self.process, None
        self.proxy = None
        if process is not None and process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=2)
        self._report("stopped")


runtime = TorRuntime()
atexit.register(runtime.stop)
