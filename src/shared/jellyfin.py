"""Optional, batched Jellyfin change notifications through the app's async core."""
from __future__ import annotations

import asyncio
import os
from pathlib import Path, PurePosixPath, PureWindowsPath
from urllib.parse import urlsplit

from .library_export import _atomic_write
from .paths import shared_data_dir

_batches: dict[tuple, tuple[list[str], asyncio.Task]] = {}


def save_api_key(token: str) -> None:
    path = shared_data_dir() / "jellyfin-api-key"
    path.parent.mkdir(parents=True, exist_ok=True)
    if not token.strip():
        path.unlink(missing_ok=True)
        return
    if any(char in token for char in '\r\n"'):
        raise ValueError("Invalid Jellyfin API key")
    _atomic_write(path, token.strip().encode())
    if os.name != "nt":
        path.chmod(0o600)


def api_key() -> str:
    token = os.environ.get("PORNFETCH_JELLYFIN_API_KEY", "").strip()
    path = shared_data_dir() / "jellyfin-api-key"
    if not token and path.is_file():
        token = path.read_text().strip()
    if not token or any(char in token for char in '\r\n"'):
        raise ValueError("Configure a Jellyfin API key")
    return token


def server_path(path: Path, local_root: str, remote_root: str) -> str:
    if not local_root.strip() or not remote_root.strip():
        raise ValueError("Configure both Jellyfin path roots")
    relative = path.resolve().relative_to(Path(local_root).expanduser().resolve())
    root = PureWindowsPath(remote_root) if "\\" in remote_root or ":" in remote_root else PurePosixPath(remote_root)
    if not root.is_absolute():
        raise ValueError("Jellyfin's server path must be absolute")
    return str(root.joinpath(*relative.parts))


async def notify_jellyfin(path: Path, settings) -> None:
    url = settings.jellyfin_url.strip().rstrip("/")
    parsed = urlsplit(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc or parsed.username or parsed.password or parsed.query or parsed.fragment:
        raise ValueError("Enter a Jellyfin HTTP(S) server URL without credentials or query parameters")
    mapped = server_path(path, settings.jellyfin_local_root, settings.jellyfin_server_root)
    token = api_key()
    routing = getattr(settings, "service_transport", "direct")
    key = (asyncio.get_running_loop(), url, token, routing)
    if key not in _batches:
        pending = []

        async def flush():
            try:
                await asyncio.sleep(0.25)
                paths = list(dict.fromkeys(pending))
                _batches.pop(key, None)
                from base_api.modules.config import RuntimeConfig

                from .tor_transport import MediaCore
                configuration = RuntimeConfig()
                configuration.timeout = 15
                configuration.request_attempts = 1
                # Dedicated session: no provider cookies, auth, proxies or locale.
                # MediaCore still enforces tor_all without a direct fallback.
                configuration.service_transport = routing
                async with MediaCore(configuration=configuration) as core:
                    response = await core.request(url + "/Library/Media/Updated", method="POST", allow_redirects=False,
                                       headers={"Authorization": f'MediaBrowser Token="{token}"'},
                                       json_data={"Updates": [{"Path": item, "UpdateType": "Created"}
                                                              for item in paths]})
                    if not 200 <= response.status_code < 300:
                        raise RuntimeError("Jellyfin did not accept the change notification")
            finally:
                if key in _batches and _batches[key][1] is asyncio.current_task():
                    _batches.pop(key, None)

        task = asyncio.create_task(flush())
        _batches[key] = pending, task
    pending, task = _batches[key]
    pending.append(mapped)
    await asyncio.shield(task)
