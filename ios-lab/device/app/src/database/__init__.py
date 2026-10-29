"""Qt-free PocketBase persistence services."""
from .client import PocketBaseClient
from .errors import PocketBaseError
from .installer import (
    DEFAULT_POCKETBASE_VERSION,
    check_system_path,
    download_and_extract_pocketbase,
    get_default_bin_dir,
    get_pocketbase_download_url,
    install_pocketbase,
    resolve_platform,
    verify_pocketbase_binary,
)
from .service import PocketBaseService
from .tracker import PocketBaseTracker

__all__ = [
    "DEFAULT_POCKETBASE_VERSION",
    "PocketBaseClient",
    "PocketBaseError",
    "PocketBaseService",
    "PocketBaseTracker",
    "check_system_path",
    "download_and_extract_pocketbase",
    "get_default_bin_dir",
    "get_pocketbase_download_url",
    "install_pocketbase",
    "resolve_platform",
    "verify_pocketbase_binary",
]
