# FAQ


## Q: Is using Porn Fetch legal?

No, Porn Fetch is against the "Terms of Services" (ToS) of the websites it supports downloading from. It's not against the law,
but against the ToS and the website owners may decide to take legal actions against users or maybe even against this project.
We are in a very "gray" area here. Porn Fetch was made to download videos for offline usage, NOT for stealing copyright protected content
in a mass. Please do not use Porn Fetch to massively scrape websites to distribute videos.

I can't prevent you from doing this, but if you want this project to keep alive, please use it fairly.

## Q: Why is downloading videos on Windows so slow compared to my internet speed?

Because Windows network I/O handling is just bad. We are using over 20 simultaneous threads to handle fetching segments
with very high speed, and Windows just can't process that really well.


## Q: Do I need to log in into my PornHub account? 

No, you can. Logging in into your PornHub account allows you to fetch videos based on your account history, but it's not
mandatory. Just a feature.

## Q: Why can the total progressbar not track the progress of all websites?

Because some websites are using HLS streaming and some are just using a Content Delivery Network. HLS streaming basically
splits videos into segments to allow a variable bitrate. The total number of segments is used to determine the total amount
of progress. Since some websites don't use HLS streaming (for good reasons), the progress tracking would be different, and it doesn't
make sense to mix them. I don't want to go in too much detail, but it has its reasons.
