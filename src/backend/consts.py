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