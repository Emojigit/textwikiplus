import requests
defwiki = {
    "zhwp": "https://zh.wikipedia.org/w/api.php",
    "enwp": "https://en.wikipedia.org/w/api.php",
    "metawm": "https://meta.wikimedia.org/w/api.php",
    "testwp": "https://test.wikipedia.org/w/api.php",
}

def chroot():
    while True:
        try:
            root = input("Please enter the root, or use `deflist` to get a list of default wikis: ")
            if root == "deflist":
                for x, y in defwiki.items():
                    print(x+" : "+y)
            else:
                for x, y in defwiki.items():
                    if root == x:
                        return y
                if root == "":
                    continue
                a = None
                try:
                    a = requests.get(root)
                except requests.exceptions.MissingSchema:
                    print("Invalid URL. Maybe you forgot `https://`?")
                    continue
                except requests.exceptions.ConnectionError:
                    print("Error while connecting to the server. Maybe the URL is incorrect?")
                    continue
                if a.status_code != 200:
                    print("HTTP error while getting the page: " + str(a.status_code) + " " + a.reason)
                    continue
                return root
        except KeyboardInterrupt:
            print()
            pass
