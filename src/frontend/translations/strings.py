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
    download_model_placeholder = "Enter a Model / Channel / Actress / Creator URL"


class TRANSLATE_PAGE_LOGIN:
    login_email_placeholder = "Enter your PornHub E-Mail address"
    login_email_password = "Enter your PornHub Password (Your account data will never be saved nor shared) "


class TRANSLATE_PAGE_SETTINGS:
    settings_button_reset_pf = "Reset Porn Fetch to default settings"
    settings_button_install_pf = "Install Porn Fetch"
    settings_button_uninstall_pf = "Uninstall Porn Fetch"


class TRANSLATE_ERRORS:
    invalid_input = """
The URL / Input you provided seems to be invalid. You either did a mistake while copy-pasting the URL e.g., missing
https://, or the website is not yet supported. 

You can create a GitHub Issue to ask for a site to be added, but specific conditions apply to that:
https://echteralsfake.me/add_site_conditions"""
    cookies_not_found = """
I could not extract the cookies for your requested page. This can happen to multiple reasons:
1) You are not authenticated in your OS
2) You are not actually logged in at the target website
3) The browser_cookie3 library had an error
4) Your browser is currently open and the database is therefore locked (try to close your browser)
5) My regular expression failed (unlikely cuz I don't do mistakes)"""
    installation_file_not_found = """
I could not find the actual Porn Fetch executable that Nuitka extracts. This is a serious issue! 
Please report it immediately on GitHub.

The only fix is, to run Porn Fetch in portable mode. """
    installation_copy_failed = """
Could not copy the Porn Fetch executable to the target installation directory.
This should not happen, please report it!"""
    installation_unsupported = """
You are likely trying to install Porn Fetch on an unsupported platform e.g., macOS / Android! 
If you think this is an error, please report it!
"""