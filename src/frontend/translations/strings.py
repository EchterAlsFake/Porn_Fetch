"""
This file basically offloads all translatable strings from the main GUI, so that I can re-use them if needed, but also
mark them translatable here, and it's just better for overall

"""
from src.backend.config import __version__

class TRANSLATE_MAIN:
    title = f"Porn Fetch v{__version__} Copyright (C) Johannes Habel 2023-2026"

class TRANSLATE_PAGE_DOWNLOAD:
    download_url_placeholder = "Enter a Video URL or an XHamster Short"
    download_playlist_placeholder = "Enter a PornHub / XVideos Playlist URL"
    download_model_placeholder = "Enter a Model / Channel / Actress / Creator URL "
    download_search_videos = "Search for videos on a website"
    download_combobox_websites_mapping = {
        0: "HQPorner",
        1: "PornHub",
        2: "EPorner",
        3: "Xvideos",
        4: "XHamster",
        5: "XNXX",
        6: "Spankbang",
        7: "MissAV",
        8: "YouPorn",
        9: "Porntrex",
    }


class TRANSLATE_PAGE_TOOLS:
    tools_groupbox_hqporner = "HQPorner"
    tools_groupbox_eporner = "EPorner"
    tools_label_get_top_porn = "Get Top Porn"
    tools_button_brazzers_videos = "Brazzers"

class TRANSLATE_PAGE_LOGIN:
    login_email_placeholder = "Enter your PornHub E-Mail address"
    login_email_password = "Enter your PornHub Password (Your account data will never be saved nor shared) "

class TRANSLATE_PAGE_TEXTBROWSER:
    tools_textbrowser_supported_sites = "Running in anonymous mode, please deactivate to display..."

class TRANSLATE_PAGE_SETTINGS:
    settings_button_reset_pf = "Reset Porn Fetch to default settings"
    settings_button_install_pf = "Install Porn Fetch"
    settings_button_uninstall_pf = "Uninstall Porn Fetch"

