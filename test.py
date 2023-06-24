from phub import Client

c = Client(language="en")
video = c.get("https://de.pornhub.com/view_video.php?viewkey=648c48bbd0f93")

title = video.views
print(title)