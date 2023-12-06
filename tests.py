from phub import Client

c = Client(language="en")
url = "https://de.pornhub.com/model/candy-love"
type_one = c.get_user(url).info
for key in type_one:
    print(key)

print(len(type_one))
