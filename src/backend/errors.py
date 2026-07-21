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
    def __init__(self, msg: str = TRANSLATE_ERRORS.):
        super().__init__(msg)
        self.msg = msg
