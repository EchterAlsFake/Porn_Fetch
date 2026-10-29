"""Database-specific exceptions."""


class PocketBaseError(RuntimeError):
    """Raised when the embedded PocketBase service or API request fails."""
