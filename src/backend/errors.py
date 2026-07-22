from frontend.translations.strings import TRANSLATE_ERRORS

class InvalidInput(Exception):
    def __init__(self, msg=TRANSLATE_ERRORS.invalid_input):
        super().__init__(msg)
        self.msg = msg


class CookiesNotFound(Exception):
    def __init__(self, msg: str = TRANSLATE_ERRORS.cookies_not_found):
        super().__init__(msg)
        self.msg = msg


class LoginError(Exception):
    def __init__(self, msg: str):
        super().__init__(msg)
        self.msg = msg


class UnsupportedPlatform(Exception):
    def __init__(self, msg: str = TRANSLATE_ERRORS.installation_unsupported):
        super().__init__(msg)
        self.msg = msg


class SomethingStupidHappened(Exception):
    def __init__(self, msg: str = TRANSLATE_ERRORS.something_stupid_happened):
        super().__init__(msg)
        self.msg = msg


class AppNetworkError(Exception): pass
class AppNotFoundError(Exception): pass
class AppBotBlocked(Exception): pass
class AppDownloadFailed(Exception): pass


async def safe_api_call(func, *args, **kwargs):
    """A wrapper that translates any provider's error into your app's standard error."""
    try:
        return await func(*args, **kwargs)
    except Exception as e:
        name = type(e).__name__
        if "Network" in name or "Proxy" in name:
            raise AppNetworkError(str(e)) from e
        elif "NotFound" in name:
            raise AppNotFoundError(str(e)) from e
        elif "BotProtection" in name:
            raise AppBotBlocked(str(e)) from e
        elif "DownloadFailed" in name:
            raise AppDownloadFailed(str(e)) from e

        raise