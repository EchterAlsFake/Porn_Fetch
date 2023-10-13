import os

from configparser import ConfigParser
from hue_shift import return_color, reset
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
        print(f"{return_color()} : DEBUG : {reset()} : {return_color()}MSG :{reset()}{return_color()} {msg}{reset()}")

    elif level == 1:
        print(f"{return_color()} : ERROR : {reset()} : {return_color()}MSG :{reset()}{return_color()} {msg}{reset()} ")


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
