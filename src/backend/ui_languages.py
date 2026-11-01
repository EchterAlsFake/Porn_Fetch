"""One registry for GUI settings, catalogs and translation tooling (no Qt dependency)."""
# Keep legacy order: older settings stored the position in this list.
LANGUAGES = (
    ("system", "System default", None),
    ("en", "English", "en"),
    ("de_DE", "Deutsch", "de_DE"),
    ("zh_CN", "简体中文", "zh_CN"),
    ("fr", "Français", "fr"),
    ("it", "Italiano", "it"),
)
TRANSLATION_HELP_URL = "https://github.com/EchterAlsFake/Porn_Fetch/blob/master/docs/TRANSLATING.md"


def catalog_for_locale(name):
    """Match regions without silently substituting Simplified for Traditional Chinese."""
    name = name.replace("-", "_")
    if name.startswith("zh"):
        return "zh_CN" if name in {"zh", "zh_CN", "zh_SG", "zh_Hans"} or "Hans" in name else None
    for code, _, catalog in LANGUAGES[1:]:
        if name == code or (code != "zh_CN" and name.split("_")[0] == code.split("_")[0]):
            return catalog
    return None
