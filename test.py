import phub

user = "https://de.pornhub.com/pornstar/june-liu"


def test_video(url):
    viewkey = url.split("=")
    viewkey = viewkey[1]
    print(viewkey)
