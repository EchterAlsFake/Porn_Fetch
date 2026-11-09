"""Document-tree storage and picker-free Android shared Downloads exports."""
import asyncio
import json
import os
import uuid
from pathlib import Path

from PySide6.QtCore import QDir, QFile, QFileSystemWatcher, QIODevice, QUrl

SHARED_DOWNLOADS = "mediastore:Download/Porn Fetch"


def shared_downloads_available() -> bool:
    private = os.environ.get("ANDROID_PRIVATE")
    if not private:
        return False
    try:
        return json.loads((Path(private) / "storage-capabilities.json").read_text())["sharedDownloads"] is True
    except (OSError, ValueError, KeyError, TypeError):
        return False


async def save_shared_download(source: Path, skip_existing: bool) -> str:
    """Await the native export without blocking Qt or requesting broad storage access."""
    if not shared_downloads_available():
        raise OSError("Android shared Downloads is unavailable. Choose an output folder instead.")
    directory = Path(os.environ["ANDROID_PRIVATE"]) / "storage-requests"
    directory.mkdir(exist_ok=True)
    identifier = uuid.uuid4().hex
    request = directory / f"{identifier}.request.json"
    response = directory / f"{identifier}.result.json"
    staged = directory / f"{identifier}.tmp"
    finished = asyncio.get_running_loop().create_future()
    watcher = QFileSystemWatcher([str(directory)])

    def read_result(*_):
        if finished.done() or not response.is_file():
            return
        try:
            value = json.loads(response.read_text())
            if value.get("ok") is not True:
                raise OSError(value.get("error") or "Android could not save the shared download.")
            uri = value["uri"]
            if not isinstance(uri, str) or not uri.startswith("content://"):
                raise ValueError("Android returned an invalid shared-download URI.")
        except (OSError, ValueError, KeyError, TypeError) as error:
            finished.set_exception(error)
        else:
            finished.set_result(uri)

    watcher.directoryChanged.connect(read_result)
    try:
        staged.write_text(json.dumps({"source": str(source.resolve()), "skipExisting": skip_existing}))
        staged.replace(request)
        # A result can arrive before the directory-change callback is dispatched.
        read_result()
        async with asyncio.timeout(3600):
            return await finished
    finally:
        watcher.directoryChanged.disconnect(read_result)
        watcher.deleteLater()
        request.unlink(missing_ok=True)  # The native copy checks this for cancellation.
        response.unlink(missing_ok=True)
        staged.unlink(missing_ok=True)


def folder_destination(folder: QUrl, filename: str) -> str:
    if folder.scheme() == "content":
        # Keep the provider's opaque document ID intact and encode the new name
        # as one URI segment (titles can contain %, #, spaces or Unicode).
        return (folder.toString(QUrl.ComponentFormattingOption.FullyEncoded).rstrip("/")
                + "/" + bytes(QUrl.toPercentEncoding(filename)).decode("ascii"))
    if folder.isLocalFile():
        return QDir(folder.toLocalFile()).filePath(filename)
    raise ValueError("Choose a folder from the system picker.")


def copy_download_file(source: Path, target_path: str) -> None:
    if not target_path.startswith("content://") and Path(target_path).resolve() == source.resolve():
        return
    # Open the source first, so a missing download cannot truncate the destination.
    with source.open("rb") as downloaded:
        target = QFile(target_path)
        if not target.open(QIODevice.OpenModeFlag.WriteOnly | QIODevice.OpenModeFlag.Truncate):
            raise OSError(target.errorString())
        try:
            while chunk := downloaded.read(1024 * 1024):
                offset = 0
                while offset < len(chunk):
                    written = target.write(chunk[offset:])
                    if written <= 0:
                        raise OSError(target.errorString())
                    offset += written
            if not target.flush():
                raise OSError(target.errorString())
        finally:
            target.close()
