"""Porn Fetch presentation for the PornHub API's download recovery."""
from base_api import DownloadConfigHLS, DownloadConfigRAW
from pornhub_api.modules.errors import SourcesUnavailable

UNAVAILABLE_MESSAGE = (
    "PornHub did not provide a working HLS or MP4 download after 8 page refreshes. "
    "This is an issue with PornHub's video servers, not Porn Fetch. "
    "There is no fix available in Porn Fetch for this server-side failure. Please try again later."
)


class PornHubSourcesUnavailable(Exception):
    """Present an exhausted provider recovery without exposing CDN URLs."""

    def __init__(self):
        super().__init__(UNAVAILABLE_MESSAGE)


async def download(video, hls: DownloadConfigHLS, raw: DownloadConfigRAW, *, on_raw=None):
    try:
        return await video.download(hls, backup_configuration=raw, on_raw=on_raw)
    except SourcesUnavailable as error:
        raise PornHubSourcesUnavailable() from error
