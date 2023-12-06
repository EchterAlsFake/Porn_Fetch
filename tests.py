from phub import Client

c = Client(language="en")
url = "https://de.pornhub.com/view_video.php?viewkey=655c5f7ab4deb"
video = c.get(url)
print(video.orientation)

