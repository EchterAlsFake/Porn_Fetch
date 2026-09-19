"""Compatibility launcher for the QML desktop application."""

from src.backend.application import Backend, ProcessVideos, main

__all__ = ["Backend", "ProcessVideos", "main"]


if __name__ == "__main__":
    main()
