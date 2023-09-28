import os

from colorama import *
from configparser import ConfigParser
data = """
[License]
accept = false

[Porn_Fetch]
default_quality = best
default_path = ./
default_threading = multiple
api_language = en
delay = false
hd = true
sort = false
sort_time = false
production = false
excluded_categories = 
categories = 
search_limit = 50

[UI]
language = en
"""


def logging(msg, level=0):

    if level == 0:
        print(f"{Fore.LIGHTCYAN_EX} : DEBUG : {Fore.RESET} : MSG : {msg}")

    elif level == 1:
        print(f"[{Fore.LIGHTRED_EX} : ERROR : {Fore.RESET} : MSG : {msg} ")


def strip_title(title):
    disallowed_chars = ["<", ">", ":", '"', "/", "\\", "|", "*", "0", "(", ")", "!", "?"]

    for disallowed_char in disallowed_chars:
        title = str(title.replace(disallowed_char, ""))

    return title


def setup_config_file(force=False):
    sections = ['License', "Porn_Fetch", "UI"]
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

    return True
