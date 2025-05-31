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