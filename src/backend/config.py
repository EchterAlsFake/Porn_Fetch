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
__version__ = "3.7"
__build__ = "desktop"  # android or desktop
__author__ = "Johannes Habel"
__next_release__ = "3.8"
__type__ = "source"
__bundle_id__ = "me.echteralsfake.pornfetch"
__org__ = "EchterAlsFake"
PUBLIC_KEY_B64 = 'zGUmG8Z5InvoYIwnIokQi+SysjEodvfP8kLoCur3KjM=' # This is the public key for the license verification
