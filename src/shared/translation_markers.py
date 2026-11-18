"""Mark shared English copy for Qt's extractor without importing Qt."""


def QT_TRANSLATE_NOOP(context: str, source: str) -> str:
    return source
