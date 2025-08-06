"""
This file stores the main instance of Porn Fetch's configuration file,
so that only one instance is active, preventing memory errors and disk
overwriting when different classes hold their own instances and overwrite
each other.
"""

# config.py
from configparser import ConfigParser

shared_config = ConfigParser()
shared_config.read("config.ini")
__license__ = "GPL 3"
__version__ = "3.6"
__build__ = "desktop"  # android or desktop
__author__ = "Johannes Habel"
__next_release__ = "3.7"

"""
This stores some values that are shared between all files. One example is the http log IP and port. Please
note that I only need this for Android development, as this is the only proper way of logging and debugging
on Android.

In a production release, these values will need consent of you, before logging is applied. Porn Fetch will never
log to any server without your explicit consent.
"""
"""
http_log_ip = "echteralsfake.duckdns.org"
http_log_port = 443
"""

http_log_ip = None
http_log_port = None
