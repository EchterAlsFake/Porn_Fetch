import subprocess
import phub
import os
client = phub.Client(language="en") # Language is en as default, but you

"""
client = phub.Client(language="en") # Language is en as default, but you can change it.
url = "https://de.pornhub.com/view_video.php?viewkey=ph6163cdeb4f815" # This URL will be used for all tests

video = client.get(url)"""
# The following is a test for M3U Downloads. It's maybe faster than the original .download method, but needs additional
# Setup.  I try it first and maybe implement it later in a few weeks.



# Tests for the Searching function
"""
record = client.search(query="hongkongdoll")
print(f"Found: {len(record)} videos")
for video in record:
    print(video.title)
"""

# Test successfully passed

"""
Idea is to implement an additional tab in the GUI for searching and downloading selected videos.
Although this won't be easy for me -_-
"""


# Test:

url = "https://www.pornhub.com/view_video.php?viewkey=ph622e6ec378a8e"
url2 = "https://de.pornhub.com/view_video.php?viewkey=64747e4fb4e1e"
video = client.get(url)
print(video.title)

