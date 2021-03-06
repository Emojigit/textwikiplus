import requests
from tqdm import tqdm
URL = ["https://zh.wikipedia.org/w/api.php"]
def chroot(root):
    URL[0] = root
DEBUG = [False]
def setdebug(status=None):
    if status != None:
        DEBUG[0] = status
    return DEBUG

def debugctl(DATA):
    if DEBUG[0] == True:
        print("[DEBUG] printing request result:")
        print(DATA)
        print("------")

def token(S,ttype):
    PARAMS_0 = {
        'action':"query",
        'meta':"tokens",
        'type':ttype,
        'format':"json",
        'curtimestamp':True,
    }
    R = S.get(url=URL[0], params=PARAMS_0)
    DATA = R.json()
    debugctl(DATA)
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
    R = S.post(URL[0], data=PARAMS_1)
    DATA = R.json()
    debugctl(DATA)
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
    R = S.get(URL[0], params=PARAMS)
    DATA = R.json()
    debugctl(DATA)
    TS = "1970-01-01T00:00:01+00:00"
    try:
        TS = DATA["query"]["pages"][0]["revisions"][0]["timestamp"]
    except KeyError:
        pass
    try:
        try:
            tmp = DATA["query"]["pages"][0]["missing"]
            return ["",TS]
        except KeyError:
            tmp = DATA["query"]["pages"]["-1"]["missing"]
            return ["",TS]
    except TypeError:
        return [DATA["query"]["pages"][0]["revisions"][0]["slots"]["main"]["content"],TS]


def edit(S,token,title,content,summary,bot,basetimestamp,starttimestamp,minor=False): # csrf token required
    PARAMS_3 = {
        "action": "edit",
        "title": title,
        "token": token,
        "format": "json",
        "text": content,
        "summary":"Edit via [[User:Emojiwiki/TextWikiPlus|TextWikiPlus]] : "+summary,
        "bot":bot,
        "headers":{'Content-Type': 'multipart/form-data'},
        "basetimestamp":basetimestamp,
        "starttimestamp":starttimestamp,
    }
    if minor == True:
        z = PARAMS_3.copy()
        z.update({"minor":True})
        PARAMS_3 = z
    R = S.post(URL[0], data=PARAMS_3)
    DATA = R.json()
    debugctl(DATA)
    try:
        if DATA["edit"]["result"] == "Success":
            return True
        else:
            raise KeyError
    except KeyError:
        print("Error while edit: "+DATA["error"]["code"])
        print(DATA["error"]["info"])
        return False

def whoami(S):
    PARAMS = {
        "action": "query",
        "format": "json",
        "meta": "userinfo",
    }
    R = S.get(URL[0], params=PARAMS)
    DATA = R.json()
    debugctl(DATA)
    return DATA["query"]["userinfo"]

def logout(S,token): #require csrf token
    PARAMS_3 = {
        "action": "logout",
        "token": token,
        "format": "json"
    }
    R = S.post(URL[0], data=PARAMS_3)
    DATA = R.json()
    debugctl(DATA)
    if DATA == {}:
        return True
    else:
        print("Error while log out: "+DATA["error"]["code"])
        print(DATA["error"]["info"])

def revisions(S,title):
    PARAMS = {
        "action": "query",
        "prop": "revisions",
        "titles": title,
        "rvprop": "timestamp|user|comment|content|tags|ids",
        "rvslots": "main",
        "formatversion": "2",
        "format": "json",
        "rvlimit":500,
    }
    R = S.get(url=URL[0], params=PARAMS)
    DATA = R.json()
    debugctl(DATA)
    PAGES = DATA["query"]["pages"]
    try:
        tmp = PAGES[0]["missing"]
        return [False,PAGES]
    except KeyError:
        return [True,PAGES]

def rollback(S,token,title,username): #rollback token required
    PARAMS_6 = {
        "action": "rollback",
        "format": "json",
        "title": title,
        "user": username,
        "token": token,
    }
    R = S.post(URL[0], data=PARAMS_6)
    DATA = R.json()
    debugctl(DATA)
    try:
        ERR = DATA["error"]["code"]
        print("Error during rollback: "+ERR)
        print(DATA["error"]["info"])
        return
    except KeyError:
        return

def undo(S,token,title,id,bot,minor=False,reason=""): # csrf token required
    PARAMS_3 = {
        "action": "edit",
        "title": title,
        "token": token,
        "format": "json",
        "undo": id,
        "summary":"Undo edit [[Special:PermanentLink/" + str(id) + "|" + str(id) + "]] via [[User:Emojiwiki/TextWikiPlus|TextWikiPlus]]: " + reason,
        "bot":bot,
        "headers":{'Content-Type': 'multipart/form-data'},
    }
    if minor == True:
        z = PARAMS_3.copy()
        z.update({"minor":True})
        PARAMS_3 = z
    R = S.post(URL[0], data=PARAMS_3)
    DATA = R.json()
    debugctl(DATA)
    try:
        if DATA["edit"]["result"] == "Success":
            return True
        else:
            raise KeyError
    except KeyError:
        print("Error while edit: "+DATA["error"]["code"])
        print(DATA["error"]["info"])
        return False

def random(S,ns):
    PARAMS = {
        "action":"query",
        "list":"random",
        "rnlimit":1,
        "rnnamespace":0,
        "utf8":"",
        "format":"json",
        "rnnamespace":ns,
    }
    R = S.get(url=URL[0], params=PARAMS)
    DATA = R.json()
    debugctl(DATA)
    try:
        ERR = DATA["error"]["code"]
        print("Error during finding random page: "+ERR)
        print(DATA["error"]["info"])
        return
    except KeyError:
        print(DATA["query"]["random"][0]["title"])

def nsinfo(S):
    PARAMS = {
        "action": "query",
        "meta": "siteinfo",
        "formatversion": "2",
        "format": "json",
        "siprop":"namespaces",
    }
    R = S.get(url=URL[0], params=PARAMS)
    DATA = R.json()
    debugctl(DATA)
    try:
        ERR = DATA["error"]["code"]
        print("Error during getting namespace infomations: "+ERR)
        print(DATA["error"]["info"])
        return
    except KeyError:
        OSTR = "Namespace info:"
        for k, v in DATA["query"]["namespaces"].items():
            NSNAME = v["name"]
            if NSNAME == "":
                NSNAME = "(main)"
            OSTR = OSTR + "\n" + NSNAME + " ID:" + k
        print(OSTR)

def wikiinfo(S):
    PARAMS = {
        "action": "query",
        "meta": "siteinfo",
        "formatversion": "2",
        "format": "json",
        "siprop":"general",
    }
    R = S.get(url=URL[0], params=PARAMS)
    DATA = R.json()
    debugctl(DATA)
    try:
        ERR = DATA["error"]["code"]
        print("Error during getting wiki infomations: "+ERR)
        print(DATA["error"]["info"])
        return
    except KeyError:
        INFO = DATA["query"]["general"]
        RO = "False"
        if INFO["readonly"] == True:
            RO = "True"
        OSTR = "Infomations about the wiki:"
        OSTR = OSTR + "\n    Main Page: " + INFO["mainpage"]
        OSTR = OSTR + "\n    Site name: " + INFO["sitename"]
        OSTR = OSTR + "\n         Logo: " + INFO["logo"]
        OSTR = OSTR + "\n  Php Version: " + INFO["phpversion"]
        OSTR = OSTR + "\n      DB Type: " + INFO["dbtype"]
        OSTR = OSTR + "\n   DB Version: " + INFO["dbversion"]
        OSTR = OSTR + "\n     Git Hash: " + INFO["git-hash"]
        OSTR = OSTR + "\n   Git Branch: " + INFO["git-branch"]
        OSTR = OSTR + "\n    Read Only: " + RO
        OSTR = OSTR + "\n  Server Time: " + INFO["time"] + " " + INFO["timezone"]
        OSTR = OSTR + "\n  Server Name: " + INFO["servername"]
        OSTR = OSTR + "\n      Wiki ID: " + INFO["wikiid"]
        OSTR = OSTR + "\n      Favicon: " + INFO["favicon"]
        OSTR = OSTR + "\nMobile Server: " + INFO["mobileserver"]
        return OSTR

def exinfo(S):
    PARAMS = {
        "action": "query",
        "meta": "siteinfo",
        "formatversion": "2",
        "format": "json",
        "siprop":"extensions",
    }
    R = S.get(url=URL[0], params=PARAMS)
    DATA = R.json()
    debugctl(DATA)
    try:
        ERR = DATA["error"]["code"]
        print("Error during getting extensions infomations: "+ERR)
        print(DATA["error"]["info"])
        return
    except KeyError:
        OSTR = "Extensions info:"
        for v in DATA["query"]["extensions"]:
            VER = ""
            try:
                VER = v["version"]
            except KeyError:
                try:
                    VER = v["vcs-system"] + "-" + v["vcs-version"]
                except KeyError:
                    pass
            descriptionmsg = "No description message provied."
            try:
                descriptionmsg = v["descriptionmsg"]
            except KeyError:
                pass
            OSTR = OSTR + "\n" + v["name"] + " " + VER + " (" + descriptionmsg + ")"
        return OSTR

def getimage(S,iname):
    PARAMS = {
        "action": "query",
        "format": "json",
        "prop": "imageinfo",
        "titles": iname,
        "iiprop":"timestamp|user|url",
    }
    R = S.get(url=URL[0], params=PARAMS)
    DATA = R.json()
    debugctl(DATA)
    PAGES = next(iter(DATA["query"]["pages"].values()))
    IURL = [""]
    try:
        IURL[0] = PAGES["imageinfo"][0]["url"]
    except:
        print("Not a file!")
        return False
    FR = S.get(IURL[0], stream=True)
    total_size_in_bytes= int(FR.headers.get('content-length', 0))
    block_size = 1024 #1 Kibibyte
    progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
    ct = b""
    for data in FR.iter_content(block_size):
        progress_bar.update(len(data))
        ct = ct + data
    progress_bar.close()
    return ct

def userinfo(S,uname):
    PARAMS = {
        "action": "query",
        "format": "json",
        "list": "users",
        "ususers": uname,
        "usprop": "blockinfo|cancreate|centralids|editcount|emailable|gender|groupmemberships|groups|implicitgroups|registration|rights",
        "utf8": "",
    }
    R = S.get(url=URL[0], params=PARAMS)
    DATA = R.json()
    debugctl(DATA)
    try:
        ERR = DATA["error"]["code"]
        print("Error during getting extensions infomations: "+ERR)
        print(DATA["error"]["info"])
        return
    except KeyError:
        USER = DATA["query"]["users"][0]
        try:
            ERR = USER["invalid"]
            print("Error during getting extensions infomations: invalid username")
        except KeyError:
            try:
                ERR = USER["missing"]
                print("Error during getting extensions infomations: user not found")
            except KeyError:
                GSTR = ""
                for v in USER["groupmemberships"]:
                    GSTR = v["group"] + " "
                IGSTR = ""
                for v in USER["implicitgroups"]:
                    ICSTR = v + " "
                BED = "False"
                try:
                    TMP = USER["blockid"]
                    BED = "True"
                    del TMP
                except KeyError:
                    pass
                RSTR = "User Info:"
                RSTR = RSTR + "\n         Username: " + USER["name"]
                RSTR = RSTR + "\n       Edit Count: " + str(USER["editcount"])
                RSTR = RSTR + "\n      Register at: " + str(USER["registration"])
                RSTR = RSTR + "\nGroup Memberships: " + GSTR
                RSTR = RSTR + "\n  Implicit Groups: " + IGSTR
                RSTR = RSTR + "\n          Blocked: " + BED
                if BED == "True":
                    RSTR = RSTR + "\n       Blocked By: " + USER["blockedby"]
                    RSTR = RSTR + "\n     Block Reason: " + USER["blockreason"]
                    RSTR = RSTR + "\n      Block Start: " + USER["blockedtimestamp"]
                    RSTR = RSTR + "\n     Block Expiry: " + USER["blockexpiry"]
                RSTR = RSTR + "\n           Gender: " + USER["gender"]
                print(RSTR)

def emailuser(S,token,target,subj,text): # csrf token required
    PARAMS_3 = {
        "action": "emailuser",
        "target": target,
        "subject": subj,
        "text": text + "\n\nThis email was sent from https://zhwp.org/U:Emojiwiki/TextWikiPlus \nIf you found any bugs, please report them.",
        "token": token,
        "format": "json"
    }
    R = S.post(URL[0], data=PARAMS_3)
    DATA = R.json()
    debugctl(DATA)
    try:
        ERR = DATA["error"]["code"]
        print("Error during sending emails: "+ERR)
        print(DATA["error"]["info"])
        return
    except KeyError:
        pass

def usercontribs(S,uname):
    PARAMS = {
        "action": "query",
        "format": "json",
        "list": "usercontribs",
        "ucuser": uname,
        "uclimit": 50
    }
    R = S.get(url=URL[0], params=PARAMS)
    DATA = R.json()
    try:
        ERR = DATA["error"]["code"]
        print("Error during getting user contribs: "+ERR)
        print(DATA["error"]["info"])
        return [False]
    except KeyError:
        return [True,DATA["query"]["usercontribs"]]
