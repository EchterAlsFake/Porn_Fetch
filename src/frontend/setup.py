import os

from configparser import ConfigParser
from hue_shift import return_color, reset
from moviepy.editor import VideoFileClip

data = """
[License]
accept = false

[Porn_Fetch]
default_quality = best
default_path = ./
default_threading = yes
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


def approximately_equal(duration1, duration2, tolerance=5):
    """
    Check if two durations are approximately equal within a given tolerance.

    Parameters:
    - duration1, duration2: int or float, durations to compare.
    - tolerance: int or float, acceptable difference between the durations.

    Returns:
    - bool, True if durations are approximately equal, False otherwise.
    """
    return abs(duration1 - duration2) <= tolerance


def check_if_video_exists(video, output_path):
    if os.path.exists(output_path):
        logging("Found video... checking length...")
        with VideoFileClip(output_path) as clip:
            existing_duration = int(clip.duration)
            video_duration = video.duration.seconds

            logging(f"Existing video duration: {existing_duration}")
            logging(f"Video duration: {video_duration}")

            if approximately_equal(existing_duration, video_duration):
                logging("Video already exists, skipping download...")
                return True

            else:
                return False

    else:
        return False



def logging(msg, level=0):

    if level == 0:
        print(f"{return_color()} : DEBUG : {reset()} : {return_color()}MSG :{reset()}{return_color()} {msg}{reset()}")

    elif level == 1:
        print(f"{return_color()} : ERROR : {reset()} : {return_color()}MSG :{reset()}{return_color()} {msg}{reset()} ")


def strip_title(title):
    disallowed_chars = ["<", ">", ":", '"', "/", "\\", "|", "*", "(", ")", "!", "?"]

    for disallowed_char in disallowed_chars:
        title = str(title.replace(disallowed_char, ""))

    return title


def setup_config_file(force=False):
    sections = ['License', "Porn_Fetch", "UI"]
    config_file = "../config.ini"

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
