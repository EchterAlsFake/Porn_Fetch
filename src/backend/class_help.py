from PySide6.QtCore import QCoreApplication
from src.backend.shared_gui import ui_popup


def result_limit_help():
    text = QCoreApplication.translate("main", f"""
The result limit defines how many videos will be returned when performing a search or doing other operations which
involves loading multiple videos. This also affects models / channels and your liked videos. The result limit is
basically the number of videos which can be loaded into the tree widget (this thing where videos are displayed).
""", None)
    ui_popup(text)


def pornhub_delay_help():
    text = QCoreApplication.translate("main", f"""
You can set a delay between requests from you to PornHub. If you are downloading a lot of videos or experiencing 
'client.call' errors, you should enable a delay. By default the delay is turned off with the value 0

A good starting point is between 0.5 - 1.5

The longer the delay is, the longer it will take to download videos, load videos and generally do stuff.
This does NOT affect other sites!
""", None)
    ui_popup(text)


def maximal_workers_help():
    text = QCoreApplication.translate("main", f"""
The maximal workers define the amount of maximal threads which can be started when using the threaded download mode.
One thread handles downloading one segment, so (in theory) 20 threads can download 20 segments at the same time.
This can of course be helpful when you have a very fast internet connection, but when you have a poor PC or running on
Android, you should set this to a lower value.

I recommend '3' for Android and 5 for low bandwidth connections < 15000 bit/s
""", None)
    ui_popup(text)


def timeout_help():
    text = QCoreApplication.translate("main", f"""
The timeout handles the timeout for retrieving segments when using the threaded download mode. If you have a poor 
internet connection you can set this higher than 10. But this isn't required for most users!
""", None)
    ui_popup(text)


def button_semaphore_help():
    text = QCoreApplication.translate("main", f"""
The Semaphore is a tool to limit the number of simultaneous actions / downloads.

For example: If the semaphore is set to 1, only 1 video will be downloaded at the same time.
If the semaphore is set to 4, 4 videos will be downloaded at the same time. Changing this is only useful, if
you have a really good internet connection and a good system.
""", None)
    ui_popup(text)


def button_threading_mode_help():
    text = QCoreApplication.translate("main", """
The different threading modes are used for different scenarios. 

1) High Performance:  Uses a class of workers to download multiple video segments at a time. Can be really fast if you
have a very strong internet connection. Maybe not great for low end systems.

2) Default:  The default download mode will just download one video segment after the next one. If you get a lot of 
timeouts this can really slow down the process, as we need to wait the Porn sites to return the video segments.
With the High Performance method, we can just download other segments while waiting which makes it so fast.
""", None)
    ui_popup(text)


def button_directory_system_help():
    text = QCoreApplication.translate("main", """
The directory system will save videos in an intelligent way. If you download 3 videos form one Pornstar and 5 videos 
from another, Porn Fetch will automatically make folders for it and move the 3 videos into that one folder and the other
5 into the other. (This will still apply with your selected output path)

This can be helpful for organizing stuff, but is a more advanced feature, so the majority of users won't use it probably
""", None)
    ui_popup(text)


def open_file_help():
    text = QCoreApplication.translate("main", """
Create a .txt file and add URLs like this:

url1
url2
url3
...

Split them with new lines. No comma, not multiple URLs in the same line!
You can also add model URLs like this:

model#MODEL_URL

An example for a file would be:

https://de.pornhub.com/view_video.php?viewkey=ph5be76343323ff
https://de.pornhub.com/view_video.php?viewkey=ph5946e5f19585a
model#https://de.pornhub.com/pornstar/nancy-a
""", None)
    ui_popup(text)


def max_retries_help():
    text = QCoreApplication.translate("main", """
The maximal retries defines how much attempts will be used for a network request. For example if an API calls
a URL for a website there will be <AMOUNT> of attempts until an error is thrown.
""", None)
    ui_popup(text)


def skip_existing_files_help():
    text = QCoreApplication.translate("main", """
If you fetch a video and the exact same filename already exists, usually Porn Fetch would just skip this file.
If you set this option to No, then Porn Fetch instead download the video and append a random number to it.

For example you have downloaded a video called:

Spain_didnt_win_against_Germany.mp4

and you download a video with the same title, then it would append a random number to it:

Spain_didnt_win_against_Germany_118251.mp4
""", disambiguation=None)
    ui_popup(text)


def model_videos_help():
    text = QCoreApplication.translate("main", """
User uploads and featured videos are two different things. User uploads are the videos which were really uploaded
by the model and the featured videos are videos the model is part or featured in.

For example the model Nancy Ace has like 10 self uploaded which she made by herself, but she is part in like thousands
of videos from other studios.

If you choose "User Uploads", only self uploaded videos will be fetched, and the other way around :)""", None)
    ui_popup(text)


def metadata_help():
    text = QCoreApplication.translate("main", """
Metadata tags are saved inside of the file itself. These are tags that video players can read from and provide you information.
Some folder viewers also give you the ability to search files by specific metadata tags. Those tags can help organize and structure files.
Porn Fetch will by default save those tags inside of your video files. 

Tag writing is not supported for formats that are not mp4 files. Porn Fetch allows you to convert video files into other
formats, however, they use other standardization for metadata keys (a specifier), which is why I can't support other
video 'containers'. 
""")
    ui_popup(text)