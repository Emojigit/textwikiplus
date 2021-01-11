import requests
URL = "https://zh.wikipedia.org/w/api.php"

def token(S,ttype):
    PARAMS_0 = {
        'action':"query",
        'meta':"tokens",
        'type':ttype,
        'format':"json",
        'curtimestamp':True,
        }
    R = S.get(url=URL, params=PARAMS_0)
    DATA = R.json()
    LOGIN_TOKEN = DATA['query']['tokens'][ttype+'token']
    return [LOGIN_TOKEN,DATA["curtimestamp"]]

def login(S,token,uname,passwd): # require "login" type token
    PARAMS_1 = {
        'action':"login",
        'lgname':uname,
        'lgpassword':passwd,
        'lgtoken':token,
        'format':"json"
    }
    R = S.post(URL, data=PARAMS_1)
    DATA = R.json()
    status = DATA["login"]["result"]
    if status == "Success":
        print("Logged in as "+DATA["login"]["lgusername"])
        return True
    else:
        print("Login Failed because: "+status)
        return False

def getpage(S,title): # no token required
    PARAMS = {
        "action":"query",
        "prop":"revisions",
        "titles":title,
        "rvslots":"*",
        "rvprop":"content|timestamp",
        "formatversion":"2",
        'format':"json"
    }
    R = S.get(URL, params=PARAMS)
    DATA = R.json()

    # print("Page ID: "+str(page['pageid']))
    TS = "1970-01-01T00:00:01+00:00"
    try:
        TS = DATA["query"]["pages"][0]["timestamp"]
    except KeyError:
        pass
    try:
        tmp = DATA["query"]["pages"]["-1"]["missing"]
        return False
    except TypeError:
        return [DATA["query"]["pages"][0]["revisions"][0]["slots"]["main"]["content"],TS]

"""
def merge_two_dicts(x, y):
    z = x.copy()   # start with x's keys and values
    z.update(y)    # modifies z with y's keys and values & returns None
    return z
"""
def edit(S,token,title,content,summary,bot,basetimestamp,starttimestamp,minor=False): # csrf token required
    PARAMS_3 = {
        "action": "edit",
        "title": title,
        "token": token,
        "format": "json",
        "text": content,
        "summary":"Edit via API: "+summary,
        "bot":bot,
        "headers":{'Content-Type': 'multipart/form-data'},
    }
    if minor == True:
        z = PARAMS_3.copy()
        z.update({"minor":True})
        PARAMS_3 = z
    R = S.post(URL, data=PARAMS_3)
    DATA = R.json()
    # DATA["error"]["code"] have error code
    # first check DATA["edit"]["result"]
    try:
        if DATA["edit"]["result"] == "Success":
            return True
        else:
            raise KeyError
    except KeyError:
        print("Error while edit: "+DATA["error"]["code"])
        return False

def userinfo(S):
    PARAMS = {
        "action": "query",
        "format": "json",
        "meta": "userinfo",
    }
    R = S.get(URL, params=PARAMS)
    DATA = R.json()
    return DATA["query"]["userinfo"]

def logout(S,token): #require csrf token
    PARAMS_3 = {
        "action": "logout",
        "token": token,
        "format": "json"
    }
    R = S.post(URL, data=PARAMS_3)
    DATA = R.json()
    if DATA == {}:
        return True
    else:
        print("Error while log out: "+DATA["error"]["code"])

def revisions(S,title):
    PARAMS = {
        "action": "query",
        "prop": "revisions",
        "titles": title,
        "rvprop": "timestamp|user|comment|content|tags",
        "rvslots": "main",
        "formatversion": "2",
        "format": "json",
        "rvlimit":500,
    }
    R = S.get(url=URL, params=PARAMS)
    DATA = R.json()
    PAGES = DATA["query"]["pages"]

    try:
        tmp = PAGES[0]["missing"]
        return [False,PAGES]
    except KeyError:
        return [True,PAGES]
