import os
import socket
from colorama import *
import sentry_sdk
from PySide6.QtWidgets import QMessageBox

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


def setup_config_file():
    sections = ['AGB']
    config_file = "config.ini"

    if not os.path.exists(config_file):
        with open(config_file, "w") as config:
            config.write(f"""
[AGB]
agb = false
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

def ui_popup(text):
    qmsg_box = QMessageBox()
    qmsg_box.setText(str(text))
    qmsg_box.exec()

def clear():
    os.system("cls")
    os.system("clear")