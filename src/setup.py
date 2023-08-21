import os
import socket
from colorama import *
import sentry_sdk
import wget
from tqdm import tqdm
from configparser import ConfigParser
data = """

[License]
accept = false

[Porn_Fetch]
default_quality = best
default_path = ./
default_threading = multiple
api_language = en
delay = true
hd = true
sort = false
sort_time = false
production = false


[Debug]
sentry = false
logging = false

[UI]
transparency = 0
language = en

[SelectedCategories]
categories = 
"""

def logging(msg, level):

    with open("log.log", "a") as log_file:

        if level == "0":
            print(f"{Fore.LIGHTCYAN_EX} : DEBUG : {Fore.RESET} : MSG : {msg}")

        elif level == "1":
            print(f"[{Fore.LIGHTRED_EX} : ERROR : {Fore.RESET} : MSG : {msg} ")

def strip_title(title):
    disallowed_chars = ["<", ">", ":", '"', "/", "\\", "|", "*", "0", "(", ")", "!"]

    for disallowed_char in disallowed_chars:
        title = str(title).replace(disallowed_char,"")  # Fixes the OS Error from V1.8.  The error mostly happens on Windows

    return title

def get_graphics():

    os.mkdir("graphics")
    os.path.join("graphics")

    urls = ["https://raw.githubusercontent.com/EchterAlsFake/Porn_Fetch/master/graphics/checkmark.png"]

    for url in tqdm(urls, dynamic_ncols=True):
        wget.download(url, out="graphics/")

    files = ["checkmark.png"]

    for file in files:
        if not os.path.isfile(f"graphics/{file}"):
            print(logging(msg="Error downloading graphics. They won't show up in UI", level="1"))


def before_send(event):
    return {
        'exception': event.get('exception', {}),
        'level': event.get('level', 'error'),
        'platform': event.get('platform'),
    }

def enable_error_handling():
    sentry_sdk.init(

        dsn="https://a2a2b3b26356d92d2797c579a4d6b7df@o4505620073480192.ingest.sentry.io/4505620077805568",

        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production.
        traces_sample_rate=1.0,
        before_send=before_send,
    )


def check_path(path):
    return bool(os.path.exists(path))


def ask_for_sentry_cli():

    _ = input("""

Do you enable automatic error collection by sentry.io?

This collects the following:

- The Python Error (so called Traceback)
- The lines of code, in which the error happened
- may include your PC name

1) Yes I support the developer and allow the automatic data collection through Sentry.
2) No I don't want Sentry to collect errors.
""")

    if _ == "1":
        enable_error_handling()
        print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTBLUE_EX}Enabled")

    else:
        print(f"{Fore.LIGHTRED_EX}[!]{Fore.RESET}Disabled")
        return False


def setup_config_file(force=False):
    sections = ['License', "Porn_Fetch", "Debug", "UI"]
    config_file = "config.ini"

    if force or not os.path.exists(config_file):
        with open(config_file, "w") as config:
            config.write(data)
            config.close()


    conf = ConfigParser()
    conf.read("config.ini")
    for section in sections:
        if not conf.has_section(section):
            print("Config file is corrupted. Updating....")
            with open(config_file, "w") as config:
                config.write(data)
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