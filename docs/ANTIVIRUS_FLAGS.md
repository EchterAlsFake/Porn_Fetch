## The Reason
The reason for this is, that Porn Fetch isn't signed. Signing is the process of digitally verifying that a file is from a 
respective author. For example if you start Porn Fetch the Windows Smart Screen will tell you that it is from an unknown source.
The problem is, that signing costs money. If I want to go with a respected and established CA I need to pay estimated 300 dollars / euros
a year. You can probably guess that I don't have the money for this and this is not worth it.

Porn Fetch sends a request at startup to the porn sites, to check your internet connection, and it also checks for updates.
Some antivirus software think that it may send data from your device, which is why it gets flagged as a trojan.

Porn Fetch also is not known by any AV or by any browser as it only has like 7k downloads, so it's not a known software.

## Proof for not being a virus

(This explanation is also for people who are not in tech, so read carefully)

GitHub is a platform where developers can host their code. To say it extremely simple, GitHub manages your code and let people
interact with it (really simple explained). GitHub has a feature called "GitHub Actions" (CI/CD). This lets you automate things 
using a script. 

When Porn Fetch is built, the source code is converted into a binary file which is readable by machines, but not by humans. 
The problem was that I always compiled (the term for converting source to binary) my files on my own system. So nobody could verify
if I made any changes to the code before publishing it. This is of course not good, so I changed it. Now the GitHub actions are used 
to automatically convert the source code into the binary file, but here comes the best:

I am technically not able to modify this process. The code compilation in the GitHub actions is defined by the scripts which are
available under ".github/workflows" in my repository. So what you can do is, you can after every release go to the workflow
which created the binary file. (I'll link to it) and view the summary of it. The workflow file will generate
the SHA256SUM which is a unique identifier for every file, and it will put this SHA sum into the GitHub Summary.

In order to read the Summary you need to have an account on GitHub and be logged in. Unfortunately this is the easiest method
for this. After verification, you can immediately delete your account if you like.

So if you compare the SHA sum from the file from GitHub actions and the SHA sum from the releases and the SHA sum matches, then
you know that the file is by 100% the same. It's completely identical.


Now what if a hacker hacks into my account and publishes his own file? 

My files are also signed using a PGP key. Now I won't explain what this is, but basically you can do:

gpg --verify "filename.sig" "filename"

If it says something like signed by "Johannes Habel <EchterAlsFake@proton.me>" with this key ID: 1E04D0A679846BC0
then you know it was me who published it. 

> [!CRITICAL]
> There's an exception... I can currently not build macOS using GitHub actions because macOS is a very complex topic and
> I don't even have real Apple hardware myself and need to use virtualization. However, if you don't trust me in that case, 
> feel free to run Porn Fetch from source code or compile your own binary :) 


## How to get around AV
If you can't download the file because it's blocked by your antivirus or Browser you have two options:

1. Turn off any AV (this also includes the Windows defender real time protection)
2. Download the file using the terminal or a separate download manager like FDM 










