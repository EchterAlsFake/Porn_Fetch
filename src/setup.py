import os
import wget
import sentry_sdk

from colorama import *
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

[UI]
transparency = 0
language = en

[SelectedCategories]
categories = 
"""


def logging(msg, level):

    if level == "0":
        print(f"{Fore.LIGHTCYAN_EX} : DEBUG : {Fore.RESET} : MSG : {msg}")

    elif level == "1":
        print(f"[{Fore.LIGHTRED_EX} : ERROR : {Fore.RESET} : MSG : {msg} ")


def strip_title(title):
    disallowed_chars = ["<", ">", ":", '"', "/", "\\", "|", "*", "0", "(", ")", "!"]

    for disallowed_char in disallowed_chars:
        title = str(title).strip(disallowed_char)

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


def setup_config_file(force=False):
    sections = ['License', "Porn_Fetch", "Debug", "UI", "SelectedCategories"]
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