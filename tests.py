from phub import Client

c = Client(language="en")
user = c.get_user("https://de.pornhub.com/model/alina-rai")
print(user.info.keys())

