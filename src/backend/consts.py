"""
This stores some values that are shared between all files. One example is the http log IP and port. Please
note that I only need this for Android development, as this is the only proper way of logging and debugging
on Android.

In a production release, these values will of course be set to None and no messages will ever be sent to an external
server without your consent.
"""

http_log_ip = "192.168.0.19"
http_log_port = 8000
