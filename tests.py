from phub import Client


username = input(f"U:")
password = input(f"P:")


c = Client(username, password, language="en", delay=False, login=False)
c.login()

feed = c.account.feed.feed

for item in feed:
    print(item)

