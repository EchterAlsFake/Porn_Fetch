"""
Tests for the core function of the PHUB version 4
"""

from phub import Client
from phub.locals import Category, Quality
from tqdm import tqdm

quality_best = Quality.BEST
quality_half = Quality.HALF
quality_worst = Quality.WORST

c = Client(language="en")
video_url = "https://de.pornhub.com/view_video.php?viewkey=64b362c47f543" # Used for the whole testing process
pbar = None


def callback(pos, total):  # Simple progressbar from v2.6
    pbar = tqdm(total=total, dynamic_ncols=True)
    pbar.update(pos - pbar.n)
    if pos == total:
        pbar.close()
        pbar = None


"""
Stage 1:  Regular video download
Status: Passed
"""

video_object = c.get(video_url)
# video_object.download(quality=quality_best, path="./", display=callback)


"""
Stage 2: Information about Video (Objects)
Status: 12/13 Passed
"""

'''
title = video_object.title # Pass
author = video_object.author # Pass
categories = video_object.categories # Pass
date = video_object.date # Pass
duration = video_object.duration # Pass
hotspots = video_object.hotspots # Not Passed: <map object at 07xf5a809d86a0>
image = video_object.image # pass
is_vertical = video_object.is_vertical # Pass
like = video_object.like # Pass
tags = video_object.tags # Pass
pornstars = video_object.pornstars # Pass
views = video_object.views # Pass
segment = video_object.segment # Pass

print(f"""
{title}
{author}
{categories}
{date}
{duration}
{hotspots}
{image}
{is_vertical}
{like}
{tags}
{pornstars}
{views}
{segment}
""")
'''


"""
Stage 3: User Accounts
Status: Passed
"""

user = video_object.author
videos = user.videos
bio = user.bio
info = user.info

for video in videos:
    print(video.title)

print(bio)
print(info)

"""
Stage 4: Search with filters and categories
Status: Unknown
"""

"""
Stage 5: Account page
Status: Unknown
"""

"""
Stage 6: Search users
Status: Unknown 
"""