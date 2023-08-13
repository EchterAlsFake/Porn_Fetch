import os
import socket
from colorama import *
import sentry_sdk
import wget
from tqdm import tqdm
from configparser import ConfigParser

def logging(msg, level):

    if level == "0":
        print(f"{Fore.LIGHTCYAN_EX} : DEBUG : {Fore.RESET} : MSG : {msg}")

    elif level == "1":
        print(f"[{Fore.LIGHTRED_EX} : ERROR : {Fore.RESET} : MSG : {msg} ")


def strip_title(title):
    disallowed_chars = ["<", ">", ":", '"', "/", "\\", "|", "*", "0"]

    for disallowed_char in disallowed_chars:
        title = str(title).replace(disallowed_char,
                                   "")  # Fixes the OS Error from V1.8.  The error mostly happens on Windows

    return title

def get_graphics():

    os.mkdir("graphics")
    os.path.join("graphics")

    urls = ["https://raw.githubusercontent.com/EchterAlsFake/Porn_Fetch/master/graphics/c.ico",
            "https://raw.githubusercontent.com/EchterAlsFake/Porn_Fetch/master/graphics/download.ico",
            "https://raw.githubusercontent.com/EchterAlsFake/Porn_Fetch/master/graphics/medium.ico",
            "https://raw.githubusercontent.com/EchterAlsFake/Porn_Fetch/master/graphics/search.ico",
            "https://raw.githubusercontent.com/EchterAlsFake/Porn_Fetch/master/graphics/settings-colorful.ico",
            "https://raw.githubusercontent.com/EchterAlsFake/Porn_Fetch/master/graphics/checkmark.png"]

    for url in tqdm(urls, dynamic_ncols=True):
        wget.download(url, out="graphics/")

    files = ["c.ico", "download.ico", "medium.ico", "search.ico", "settings-colorful.ico", "checkmark.png"]
    
    for file in files:
        if os.path.isfile(f"graphics/{file}"):
            pass
        
        else:
            print("Error with Icon download. Icon's won't be available in the GUI!")




def enable_error_handling():
    sentry_sdk.init(

        dsn="https://a2a2b3b26356d92d2797c579a4d6b7df@o4505620073480192.ingest.sentry.io/4505620077805568",

        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production.
        traces_sample_rate=1.0

    )
    sentry_cli = True

def check_path(path):
    return True if os.path.exists(path) else False

def ask_for_sentry_cli():

    _ = input("""

Do you allow Sentry.io to collect errors within this program?

The following data are obtained:

- Error message (Python Traceback)
- Variables and their values
- In which class / function / line the error occurred.


No sensitive data / system data or user specific data that would lead to an identification is collected.

1) Yes I support the developer and allow the automatic data collection through Sentry.
2) No I don't want Sentry to collect errors.
""")

    if _ == "1":
        try:
            enable_error_handling()
            print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTBLUE_EX}Enabled")
            return True

        finally:
            pass

    else:
        print(f"{Fore.LIGHTRED_EX}[!]{Fore.RESET}Disabled")
        return False


def setup_config_file(force=False):
    sections = ['License', "Porn_Fetch", "Debug"]
    config_file = "config.ini"

    if force or not os.path.exists(config_file):
        with open(config_file, "w") as config:
            config.write(f"""
[License]
accept = false

[Porn_Fetch]
default_quality = best
default_path = ./
default_threading = multiple

[Debug]
sentry = false

""")
            config.close()


    conf = ConfigParser()
    conf.read("config.ini")
    for section in sections:
        if not conf.has_section(section):
            print("Config file is corrupted. Updating....")
            with open(config_file, "w") as config:
                config.write(f"""
            [License]
            accept = nothing_in_here

            [Porn_Fetch]
            default_quality = best
            default_path = ./
            default_threading = multiple

            [Debug]
            sentry = false

            """)
                config.close()


def internet_test():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = "pornhub.com"
    port = 443
    server_addr = (host, port)

    try:
        s.connect(server_addr)
        return True

    except ConnectionResetError:
        print(
            f"{Fore.LIGHTRED_EX}[~]{Fore.RESET}Connection to PornHub was reset. You are probably behind a firewall that blocks your request....")
        return False

    except ConnectionRefusedError:
        print(
            f"{Fore.LIGHTRED_EX}[~]{Fore.RESET}PornHub refused the connection. This can have several issues. Try if you can reach it within your browser and try again.")
        return False

    except ConnectionError:
        print(
            f"{Fore.LIGHTRED_EX}[~]{Fore.RESET}Could not connect to PornHub. Please make sure you are using a stable / secure internet connection.")
        return False

def clear():
    os.system("cls")
    os.system("clear")