from PySide6.QtCore import QCoreApplication
from src.backend.shared_gui import ui_popup


def button_help_download_mode():
    text = QCoreApplication.translate("main", """
The different threading modes are used for different scenarios. 

1) High Performance:  Uses a class of workers to download multiple video segments at a time. Can be really fast if you
have a very strong internet connection. Maybe not great for low end systems.

2) Default:  The default download mode will just download one video segment after the next one. If you get a lot of 
timeouts this can really slow down the process, as we need to wait the Porn sites to return the video segments.
With the High Performance method, we can just download other segments while waiting which makes it so fast.
""", None)
    ui_popup(text)


def button_help_simultaneous_downloads():
    text = QCoreApplication.translate("main", f"""
The Semaphore is a tool to limit the number of simultaneous actions / downloads.

For example: If the semaphore is set to 1, only 1 video will be downloaded at the same time.
If the semaphore is set to 4, 4 videos will be downloaded at the same time. Changing this is only useful, if
you have a really good internet connection and a good system.
""", None)
    ui_popup(text)


def button_help_network_delay():
    text = QCoreApplication.translate("main", f"""
You can set a delay between requests from you and a site. If you are downloading a lot of videos or experiencing 
errors, you should enable a delay. By default the delay is turned off with the value 0

A good starting point is between 0.5 - 1.5

The longer the delay is, the longer it will take to download videos, load videos and generally do stuff. This does not
really affect the high performance download mode.
""", None)
    ui_popup(text)


def button_help_maximal_workers():
    text = QCoreApplication.translate("main", f"""
The maximal workers define the amount of maximal threads which can be started when using the threaded download mode.
One thread handles downloading one segment, so (in theory) 20 threads can download 20 segments at the same time.
This can of course be helpful when you have a very fast internet connection, but when you have a poor PC or running on
Android, you should set this to a lower value.

I recommend '3' for Android and 5 for low bandwidth connections < 15000 kbit/s
""", None)
    ui_popup(text)


def button_help_timeout():
    text = QCoreApplication.translate("main", f"""
The timeout handles the timeout for retrieving segments when using the threaded download mode. If you have a poor 
internet connection you can set this higher than 10. But this isn't required for most users!
""", None)
    ui_popup(text)


def button_help_max_retries():
    text = QCoreApplication.translate("main", """
The maximal retries defines how much attempts will be used for a network request. For example if an API calls
a URL for a website there will be <AMOUNT> of attempts until an error is thrown.
""", None)
    ui_popup(text)


def button_help_speed_limit():
    text = QCoreApplication.translate("main", """
The speed limit sets the maximum allowed network speed in megabyte per seconds. However, this doesn't work perfectly.
The speed limit also only works for the default download mode, because it wouldn't make sense downloading multiple
segments at the same time with a speed limit being in place.

If you need something more 'exact / precise', use applications like NetLimiter 4 or something similar.
""", disambiguation=None)
    ui_popup(text)

def button_help_processing_delay():
    text = QCoreApplication.translate("main", """
The processing delay sets a delay before every video gets downloaded.
Let's assume you set a delay of 30 (30 seconds), then it will take 30 seconds between each video downloads.
This does not apply if you have a value of simultaneous downloads greater than 1.
""")
    ui_popup(text)


def button_help_model_videos():
    text = QCoreApplication.translate("main", """
User uploads and featured videos are two different things. User uploads are the videos which were really uploaded
by the model and the featured videos are videos the model is part or featured in.

For example the model Nancy Ace has like 10 self uploaded which she made by herself, but she is part in like thousands
of videos from other studios.

If you choose "User Uploads", only self uploaded videos will be fetched, and the other way around :)""", None)
    ui_popup(text)


def button_help_result_limit():
    text = QCoreApplication.translate("main", f"""
The result limit defines how many videos will be returned when performing a search or doing other operations which
involves loading multiple videos. This also affects models / channels and your liked videos. The result limit is
basically the number of videos which can be loaded into the tree widget (this thing where videos are displayed).
""", None)
    ui_popup(text)


def button_help_write_metadata():
    text = QCoreApplication.translate("main", """
Metadata tags are saved inside of the file itself. These are tags that video players can read from and provide you information.
Some folder viewers also give you the ability to search files by specific metadata tags. Those tags can help organize and structure files.
Porn Fetch will by default save those tags inside of your video files. 
""")
    ui_popup(text)


def button_help_directory_system():
    text = QCoreApplication.translate("main", """
The directory system will save videos in an intelligent way. If you download 3 videos form one Pornstar and 5 videos 
from another, Porn Fetch will automatically make folders for it and move the 3 videos into that one folder and the other
5 into the other. (This will still apply with your selected output path)

This can be helpful for organizing stuff, but is a more advanced feature, so the majority of users won't use it probably
""", None)
    ui_popup(text)


def button_help_skip_existing_files():
    text = QCoreApplication.translate("main", """
If you fetch a video and the exact same filename already exists, usually Porn Fetch would just skip this file.
If you set this option to No, then Porn Fetch instead download the video and append a random number to it.

For example you have downloaded a video called:

Spain_didnt_win_against_Germany.mp4

and you download a video with the same title, then it would append a random number to it:

Spain_didnt_win_against_Germany_118251.mp4
""", disambiguation=None)
    ui_popup(text)


def button_help_direct_download():
    text = QCoreApplication.translate("main", """
When you download a single video, usually you need to mark the video in the tree widget and then hit Download to
actually download it.

By activating this function we bypass the tree widget. The video will be loaded into it, but immediately self-downloaded.
So you only need to press 'Download' once and not twice. 

This makes it easier, but gives you less control.""", disambiguation=None)
    ui_popup(text)


def button_help_anonymous_mode():
    text = QCoreApplication.translate("main", """
The anonymous mode renames all of Porn Fetch's elements to look NOT like a Porn downloader.
This makes it useful for downloading Porn content if you are in public, or multiple people use your PC / Phone.

This also disables thumbnail preview. All titles will be replaced with: [redacted] as well as all authors.
""", disambiguation=None)
    ui_popup(text)


def button_help_proxy_kill_switch():
    text = QCoreApplication.translate("main", """
The proxy kill switch is an additional security layer if you use proxies. It will check your IP each time before making
a request and if it's leaked it will immediately exit everything.

My priority on developing this is low. Please do not report errors. Thank you <3
""", disambiguation=None)
    ui_popup(text)


def button_help_supress_errors():
    text = QCoreApplication.translate("main", """
If you enable this function, all errors will be suppressed. This does not mean that they will be completely ignored, but
you won't get a big notification for it. 

If you have activated Network Logging, they will still be reported. If an error happens while iterating through videos,
the current video will be skipped and Porn Fetch will continue with the next one.    
    """, disambiguation=None)
    ui_popup(text)


def button_help_network_logging():
    text = QCoreApplication.translate("main", """
I have created my own server that runs 24/7 in my home. Porn Fetch (ONLY if you enable it) logs specific types of errors,
that I don't know of, or that I need your help to fix them, to my server using a simple JSON post request.

You can see the Code of the server publicly here -->: https://github.com/EchterAlsFake/Server
Porn Fetch also does its update checking mechanism through that server.

IMPORTANT:
The server is IPv6 only. If your ISP has not given you a working IPv6 IP address, then you can't reach me.
You can check for yourself on 'https://ipleak.net'. It should be something like this: '2a02:810a:186:b400::5c51'

My server does NOT save any of your personal information. No IP addresses, no PC information, no other identifiable information.
The only things being stored is the literal Python exception that's being caught, the version you are running on, and your system.
Like literally only if you use Windows, Linux or Mac. Nothing else.

You can see that yourself, as mentioned before on the source code.
You'd help me a lot by enabling network logging :) 
""")
    ui_popup(text)


def open_file_help():
    text = QCoreApplication.translate("main", """
Create a .txt file and add URLs like this:

video#<url>
...

Split them with new lines. No comma, not multiple URLs in the same line!
You can also add model URLs like this:

model#<url>
An example for a file would be:

video#https://de.pornhub.com/view_video.php?viewkey=ph5be76343323ff
video#https://de.pornhub.com/view_video.php?viewkey=ph5946e5f19585a
model#https://de.pornhub.com/pornstar/nancy-a
""", None)
    ui_popup(text)








