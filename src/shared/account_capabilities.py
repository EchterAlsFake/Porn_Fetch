"""Account controls available in Porn Fetch, independent of provider transport."""

from dataclasses import dataclass
from typing import Literal

from .supported_websites import supported_websites
from .translation_markers import QT_TRANSLATE_NOOP


@dataclass(frozen=True, slots=True)
class AccountCollection:
    key: str
    label: str
    url_hint: str = ""


@dataclass(frozen=True, slots=True)
class AccountProvider:
    key: str
    name: str
    login: Literal["password", "tokens"] | None = None
    browser_import: Literal["cookies", "username"] | None = None
    email_required: bool = False
    collections: tuple[AccountCollection, ...] = ()


_HISTORY = AccountCollection("history", QT_TRANSLATE_NOOP("AccountPage", "Get Watch History"))
_LIKED = AccountCollection("liked", QT_TRANSLATE_NOOP("AccountPage", "Get Liked Videos"))

# Each entry describes existing application support, including any input the
# account flow needs. Sites outside this mapping use the same unavailable state.
ACCOUNT_PROVIDERS = {
    "pornhub": AccountProvider(
        "pornhub", "PornHub", "password", "username",
        collections=(
            _HISTORY,
            AccountCollection("recommended", QT_TRANSLATE_NOOP("AccountPage", "Get Recommended Videos")),
            AccountCollection("feed", QT_TRANSLATE_NOOP("AccountPage", "Get Subscription Feed")),
            AccountCollection("favorites", QT_TRANSLATE_NOOP("AccountPage", "Get Favorite Videos")),
        ),
    ),
    "xhamster": AccountProvider(
        "xhamster", "XHamster", "password", "cookies", email_required=True,
        collections=(
            _LIKED,
            AccountCollection(
                "playlist", QT_TRANSLATE_NOOP("AccountPage", "Get Playlist Videos"),
                "https://xhamster.com/my/playlists/...",
            ),
        ),
    ),
    "xvideos": AccountProvider(
        "xvideos", "XVideos", "tokens", "cookies",
        collections=(
            AccountCollection("watch_later", QT_TRANSLATE_NOOP("AccountPage", "Get Watch Later Videos")),
            _HISTORY,
            _LIKED,
        ),
    ),
}


def account_provider_key(value: str) -> str:
    """Resolve account display names and provider IDs to the same ID."""
    key = value.strip().casefold()
    return next((provider.key for provider in ACCOUNT_PROVIDERS.values()
                 if provider.name.casefold() == key), key)


def account_providers() -> tuple[AccountProvider, ...]:
    return (
        *ACCOUNT_PROVIDERS.values(),
        *(AccountProvider(site["id"], site["name"]) for site in supported_websites()
          if site["id"] not in ACCOUNT_PROVIDERS),
    )
