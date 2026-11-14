"""Premium feature limits shared by GUI and CLI entry points."""
from contextlib import aclosing
from typing import AsyncIterator, TypeVar

from src.shared.media import VideoObject

FREE_COLLECTION_PREVIEW = 5
T = TypeVar("T")


def require_library_export(premium: bool) -> None:
    if not premium:
        raise PermissionError("Media Library Export requires an active Premium license.")


def download_parallelism(requested: int, premium: bool) -> int:
    return max(1, int(requested)) if premium else 1


async def public_collection_items(items: AsyncIterator[T], premium: bool) -> AsyncIterator[T]:
    """Limit the source before filtering/ranges and close it without reading item six."""
    count = 0
    async with aclosing(items):
        async for item in items:
            yield item
            count += 1
            if not premium and count >= FREE_COLLECTION_PREVIEW:
                break


def bulk_video_requires_premium(video: VideoObject) -> bool:
    """Also protect public-collection rows prepared under an earlier entitlement."""
    return bool(video.origin_iterator_url and not video.is_from_account
                and (video.index or 0) > FREE_COLLECTION_PREVIEW)
