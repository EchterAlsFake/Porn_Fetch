"""Qt document-URI helpers for Android's system storage picker."""
from pathlib import Path

from PySide6.QtCore import QDir, QFile, QIODevice, QUrl


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
