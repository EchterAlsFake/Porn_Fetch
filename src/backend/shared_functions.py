"""
This file contains functions which are needed for the Graphical User Interface, as well as the CLI.
If you know what you do, you can change a few things here :)
"""

import os
import string
import phub.errors

from phub import Client
from colorama import Fore
from hue_shift import return_color, reset
from datetime import datetime
from moviepy.editor import VideoFileClip
from configparser import ConfigParser

"""
The following are the sections and options for the configuration file. Please don't change anything here, 
as they are indeed needed for the main applications!
"""

sections = ["Performance", "License", "Video", "UI"]
options_performance = ["threading", "semaphore", "threading_mode"]
options_video = ["quality", "language", "output_path", "directory_system", "search_limit"]
options_license = ["accepted"]
options_ui = ["language"]

"""
Explanation:

Threading Mode:

2 = High Performance
1 = FFMPEG
0 = Default

Directory System:

1 = Yes
0 = No

Semaphore:

Integer value.

If you set it to 3, three videos will be downloaded at the same time (You get the point)

"""

default_configuration = f"""

[License]
accepted = no

[Performance]
threading = yes
threading_mode = 2
semaphore = 1

[Video]
quality = best
language = en
output_path = ./
directory_system = 0
search_limit = 50

[UI]
language = en



"""


def logger_error(e):
    print(f"{datetime.now()} : {Fore.LIGHTRED_EX}[ERROR] : {reset()} : {e}")


def logger_debug(e):
    print(f"{datetime.now()} : {Fore.LIGHTCYAN_EX}[DEBUG] : {return_color()} : {e}")


def check_video(url, language, delay):
    if type(url) == "str":
        try:
            return Client(language=language, delay=delay).get(url)

        except phub.errors.URLError:
            logger_error(f"Invalid URL! : {url}")
            return False


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
        logger_debug("Found video... checking length...")
        with VideoFileClip(output_path) as clip:
            existing_duration = int(clip.duration)
            video_duration = video.duration.seconds

            logger_debug(f"Existing video duration: {existing_duration}")
            logger_debug(f"Video duration: {video_duration}")

            if approximately_equal(existing_duration, video_duration):
                logger_debug(f"Video already exists, skipping download...")
                return True

            else:
                return False

    else:
        return False


def strip_title(title):
    illegal_chars = '<>:"/\\|?*'

    # Only keep characters that are valid UTF-8 and not in the list of illegal characters
    cleaned_title = ''.join([char for char in title if char in string.printable and char not in illegal_chars])

    return cleaned_title


def setup_config_file(force=False):
    if os.path.isfile("config.ini") == False or force:
        logger_error("Configuration file is broken / not found. Automatically creating a new one with default "
                     "configuration")

        try:
            with open("config.ini", "w") as config_file:
                config_file.write(default_configuration)

        except PermissionError:
            logger_error("Can't write to config.ini due to permission issues.")
            exit(1)


    else:
        config = ConfigParser()
        config.read("config.ini")

        try:
            for idx, section in sections:

                if config.has_section(section) and idx == 0:
                    for option in options_performance:
                        if config.has_option(section=section, option=option):
                            pass

                        else:
                            setup_config_file(force=True)

                if config.has_section(section) and idx == 1:
                    for option in options_license:
                        if config.has_option(section=section, option=option):
                            pass

                        else:
                            setup_config_file(force=True)

                if config.has_section(section) and idx == 2:
                    for option in options_video:
                        if config.has_option(section=section, option=option):
                            pass

                        else:
                            setup_config_file(force=True)

                if config.has_section(section) and idx == 3:
                    for option in options_ui:
                        if config.has_option(section=section, option=option):
                            pass

                        else:
                            setup_config_file(force=True)

                else:
                    setup_config_file(force=True)

        except KeyError:
            setup_config_file(force=True)
