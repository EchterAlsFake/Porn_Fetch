# [1] / vs \
Developing software for Windows is the worst experience ever (apart from Apple of course). Not only because this whole eco-system
is legacy as fuck, but the Antivirus literally makes it impossible to develop anything as an open source developer.

First is, that whenever I want to execute a command that involves `/` I need to use a 1999 like backslash `\` 🤮 because 
Windows is THE ONLY SYSTEM that uses it. All other systems, no matter if iOS, macOS, Linux, Android or whatever have managed
to standardize the normal slash for file paths. Just Microsoft thought: "ey we are so special bro let us cook" YOU FUCKING DIDN'T HOLY SHIT

100 Lines of Porn Fetch code (including APIs) are probably ONLY made to solve this problem which wouldn't be needed if Bill Gates had at least
one working brain cell (probably got it taken from EPN, but I don't open that topic now)

So, however if you fixed that problem you can go to the next one and that is winget. Winget is so fucking slow and installing dependencies on
Windows feels like I am going back 10 years ago. Why can't every system on this planet just be like Arch Linux where I just do a lil `yay` and 
everything works.

# [2] Antivirus
This is THE ABSOLUTE BIGGEST PAIN POINT IN FUCKING HISTORY

Guys, everytime I open Porn Fetch (from source code) it takes probably 5 seconds longer than on Linux to open.
And you wanna know why? Because the god damn antivirus scans the SAME FUCKING FILES EVERY TIME I want to open them.

Microsoft, if you see this:

If I want to hack my users, it is as easy as making a "time.sleep(25)" at the beginning of my code to get around
your whole antivirus, but I ain't giving tips here for future ransomware devs, but just as an example.

It would be helpful if Microsoft had a feature or a button that you can press which is called:

`I AM THE FUCKING OWNER OF MY SYSTEM LET ME DO WHAT I FUCKING WANT YOU STUPID MORONS I PAID 150€ FOR THIS BULLSHIT SYSTEM`

So, once you finally got your app developed (on Arch Linux of course and not on this ************ legacy system) you
wanna compile the code to a final executable or in this case bundle the Python interpreter into one file.
I am using Nuitka for this and Nuitka has been around for I don't know DECADES????????????? 

And still, Windows flags the build every time. And you know, if Windows would just be like: "Hey this COULD be a virus, please
proceed with caution", NOPE, Windows thinks it's smarter than me and completely deletes random build artifacts / files DURING THE FUCKING
BUILD which makes it impossible to build anything.

Now, you could say: "Yo, but why aren't you just disabling real-time protection?"

And yes... That solves the issue.

but only for me, not for the 32.000 people that have downloaded Porn Fetch so far and probably ALL had to disable AV!!!!!!!!!!!!!

But why does other software not have this problem? Is it a skill issue????



NO IT'S A CORPORATE GREED / MONEY ISSUE. To make Windows not flag your program you need to use code signing from a CA. Basically you pay
for a certificate and then you can sign files with your identity.

The cheapest option for me would cost around 450€ for the first year + Hardware key and then 129€ for every year.
WITHOUT MAKING ANY MONEY FROM IT. 

Again... This is the CHEAPEST option.

Or all my users turn of antivirus. Sure.... (FUCK YOU WINDOWS!)

# [3] The price
If Windows was free software (like Linux) then I would say:

Well I can't complain, cuz I get it for free. But NO this shit costs 150€. 

for a system that crashes more often than <insert politically incorrect 9/11 joke>



# Solution
- Install Arch Linux!





























