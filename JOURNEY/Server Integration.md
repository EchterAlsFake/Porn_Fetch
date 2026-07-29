# Why
I need a server can handle the update checking for Porn fetch, serve as the documentation landing page for my projects
and also process the crypto payments.

Because I am working with YOUR sensitive data I did NOT want to rely on external providers / hosters where I have no control
over the data. So that's why I wanted to self-host everything


# Local ISP Trap
As you might know, Germany is a highly developed country in the EU. Well, not for the fucking internet! 
I am already in the top 7% of people in Germany who actually have gigabit internet, but in Germany, you don't get a
symmetric connection. No, I have 50mbit/s up and it's not possible to get more at my location (unless I do very specific things)

However, let's be honest, 50mbit/s up is more than enough. But I also don't get a public IPv4 Address. Yes that's right, 
I don't have my own IPv4 Address. Only IPv6. The IPv6 is behind CCGNAT which means that I am sharing the same IP Address with
other households. Therefore I can not do Port Forwarding, so you can not connect to my server directly.

This is the reason why I have Cloudflare on my site, because cloudflare handles this for free and additionally
provides me with advanced caching, higher speeds, bot protection, rules to block certain countries
The problem is that this means that Cloudflare has your IP Address when connecting to my server. 

But to be honest, if you use Porn Fetch. most of the sites use Cloudflare anyways, so they know your IP regardless.

# The Server itself (Hardware)
Originally I was hosting on an Acer Swift 3 laptop with an encrypted filesystem using Arch Linux.
This would have been fine, but the battery gave up and I can't use it anymore for safety reasons until I have that thing out
which isn't as easy cuz the screws are stuck and I can't get them out right now.

As a backup I am currently hosting on my Pixel 7 Pro which perfectly works, and actually has more processing power than 
the Acer Swift 3 and especially more RAM which is great. I have set specific tweaks to the Android System to keep
this thing 24/7 alive and it works great.

However, when I actually process payments I need to find something more reliable. I am still thinking on what I can use here.

# The Software
The Source Code is publicly accessible at: https://github.com/EchterAlsFake/Server

### Log Policy
There is no logging. I have disabled everything, seriously and none of you data is saved except for the payment stuff
of course but I am required by law to do this, so yeah. 

# The Hidden Domain
In some countries Porn is actually banned e.g., South Korea. People from those countries should also be able to use
Porn Fetch which is the reason why I also made a darknet domain for my server and website. 

Porn Fetch can (v3.9+) connect to my server completely anonymous over the Darknet. 

Is this Illegal?
No!