"""
This file contains functions which are needed for the Graphical User Interface, as well as the CLI.
If you know what you do, you can change a few things here :)
"""


import os
import sys
import string

import phub.errors
from phub import Client, locals, errors
from colorama import Fore
from hue_shift import return_color, reset
from time import sleep
from datetime import datetime
from moviepy.editor import VideoFileClip


"""
The following are the sections and options for the configuration file. Please don't change anything here, 
as they are indeed needed for the main applications!
"""

sections = []
options = []




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

    for idx, section in sections:
        ""

        # Need to finish settings widget first




