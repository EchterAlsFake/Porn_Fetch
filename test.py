import phub

user = "https://de.pornhub.com/view_video.php?viewkey=ph5e6be719d708c"

c = phub.Client(language="en")
x = c.get(user)
print(x.like)
