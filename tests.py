from phub import Client, HTMLQuery, JSONQuery, SubQuery, PSQuery

c = Client(language="en")
search = c.search("Mia Khalifa", feature=HTMLQuery)


for video in search[0:10]:
    print(video.title)