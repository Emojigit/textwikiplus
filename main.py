import mwng as mw
import cmd2, editor

class App(cmd2.Cmd):

    C_MW = "MediaWiki Commands"

    def __init__(self,wiki):
        super().__init__()
        self.prompt="TWP> "
        self.site = wiki
        self.API = mw.API(wiki)

    @cmd2.with_category(C_MW)
    @cmd2.with_argument_list
    def do_login(self,args):
        """Use botpassword to login"""
        user = args[0]
        botpassword = self.read_input(prompt="Enter the botpassword: ") if len(args) == 1 else args[1]
        self.poutput("Received: {} ({})".format(user,botpassword))
        try:
            DATA = self.API.login(user,botpassword)
        except mw.MWLoginError as e:
            reason = e.dump["login"]["reason"]["*"]
            self.poutput("Login failed: " + reason)
            if self.debug:
                self.poutput("Request: {}\nRespond: {}".format(e.request,e.dump))
        else:
            self.poutput("Login Success. ({})".format(DATA["login"]["lgusername"]))

    def parse_userinfo(self,userinfo,whoami: bool = True):
        username = userinfo["name"]
        if "anon" in userinfo:
            username = "Anon (IP: {})".format(userinfo["name"])
        if whoami:
            self.poutput("Current user info:")
        else:
            self.poutput("User info:")
        self.poutput("Username: {}".format(username))
        if "registrationdate" in userinfo:
            self.poutput("Registered at: {}".format(userinfo["registrationdate"]))
        self.poutput("Groups: {}".format(", ".join(userinfo["groups"])))
        if whoami:
            self.poutput("Email Address: {}".format((userinfo["email"] + " ({})".format(userinfo["emailauthenticated"] if "emailauthenticated" in userinfo else "False")) if userinfo["email"] != "" else "[None]"))
            self.poutput("Last contributed: {}".format(userinfo["latestcontrib"] if "latestcontrib" in userinfo else "[None]"))
        if "blockid" in userinfo:
            self.poutput("Blocked: True (ID: {})".format(userinfo["blockid"]))
            self.poutput("Blocked by: {}".format(userinfo["blockedby"]))
            self.poutput("Block reason: {}".format(userinfo["blockreason"] if userinfo["blockreason"] != "" else "[None]"))
            self.poutput("Block started: {}".format(userinfo["blockedtimestamp"]))
            self.poutput("Block end: {}".format(userinfo["blockexpiry"]))

    @cmd2.with_category(C_MW)
    def do_whoami(self,_):
        """Get your own account/IP information"""
        req = {
            "action": "query",
            "meta": "userinfo",
            "uiprop": "*" # "|".join(["blockinfo","groups","editcount","ratelimits","email","registrationdate","latestcontrib"])
        }
        try:
            DATA = self.API.get(req)
        except mw.MWAPIError as e:
            self.poutput("Error during getting user info: " + e.message)
            if self.debug:
                self.poutput("Request: {}\nRespond: {}".format(e.request,e.dump))
        else:
            userinfo = DATA["query"]["userinfo"]
            self.parse_userinfo(userinfo)

    @cmd2.with_category(C_MW)
    def do_userinfo(self,arg):
        """Get user info by name"""
        req = {
            "action": "query",
            "list": "users",
            "ususers": arg,
            "usprop": "|".join(["blockinfo","groups","editcount","ratelimits","registrationdate","latestcontrib"])
        }
        try:
            DATA = self.API.get(req)
        except mw.MWAPIError as e:
            self.poutput("Error during getting user info: " + e.message)
            if self.debug:
                self.poutput("Request: {}\nRespond: {}".format(e.request,e.dump))
        else:
            USER = DATA["query"]["users"][0]
            if "invalid" in USER:
                self.poutput("Error during getting user info: Invalid username")
            elif "missing" in USER:
                self.poutput("Error during getting user info: Not found")
            else:
                self.parse_userinfo(USER,False)

    @cmd2.with_category(C_MW)
    def do_logout(self, arg):
        """Logout from the MediaWiki site"""
        try:
            DATA = self.API.logout()
        except mw.MWAPIError:
            self.poutput("Error during logout: " + e.message)
            if self.debug:
                self.poutput("Request: {}\nRespond: {}".format(e.request,e.dump))
        else:
            self.poutput("Logout done.")

    @cmd2.with_category(C_MW)
    def do_view(self,arg):
        """Get the content of a page"""
        req = {
            "action":"query",
            "prop":"revisions",
            "titles":arg,
            "rvslots":"*",
            "rvprop":"content",
        }
        try:
            DATA = self.API.get(req)
        except mw.MWAPIError as e:
            self.poutput("Error during getting page: " + e.message)
        else:
            pages = DATA["query"]["pages"]
            if "-1" in pages and "missing" in pages["-1"]:
                self.poutput("Page not found.")
            else:
                page = pages[tuple(pages.keys())[0]]
                content = page["revisions"][0]["slots"]["main"]["*"]
                self.poutput(content)

    @cmd2.with_category(C_MW)
    def do_edit(self,arg):
        """Edit a MediaWiki page"""
        whoami_req = {
            "action": "query",
            "meta": "userinfo",
        }
        whoami = self.API.get(whoami_req)
        if "anon" in whoami["query"]["userinfo"]:
            if self.read_input(prompt="Not logged in. Still wanna edit? (y/N) ").upper()[0] != "Y":
                self.poutput("Cancled.")
                return
        cont_req = {
            "action":"query",
            "prop":"revisions",
            "titles":arg,
            "rvslots":"*",
            "rvprop":"content",
        }
        cont = "<!-- Page not found. Remove this line and start editing. -->\n"
        try:
            cont_DATA = self.API.get(cont_req)
        except mw.MWAPIError as e:
            self.poutput("Error during getting page: " + e.message)
            if self.debug:
                self.poutput("Request: {}\nRespond: {}".format(e.request,e.dump))
        else:
            pages = cont_DATA["query"]["pages"]
            if "-1" in pages and "missing" in pages["-1"]:
                pass
            else:
                page = pages[tuple(pages.keys())[0]]
                cont = page["revisions"][0]["slots"]["main"]["*"]
                token, ts = self.API.csrf()
                if self.debug:
                    self.poutput("Token: {}\nTimestamp: {}".format(token,ts))
            while True:
                cont = editor(text=cont)
                try:
                    confirm = self.read_input(prompt="Confirm? (Y)es, (N)o or (A)bort. ").upper()[0]
                except IndexError:
                    confirm = "N"
                if confirm == "Y":
                    summary = self.read_input(prompt="Please enter the summary: ")
                    try:
                        minor = self.read_input(prompt="Minor edit? (y/N) ").upper()[0] == "Y"
                    except IndexError:
                        minor = False
                    try:
                        DATA = self.API.edit(arg,{"text": cont, "minor": minor if minor else None},summary,token,ts)
                    except mw.MWAPIError as e:
                        self.poutput("Error during editing page: " + e.message)
                        if self.debug:
                            self.poutput("Request: {}\nRespond: {}".format(e.request,e.dump))
                    else:
                        self.poutput("Done. {}".format(DATA if self.debug else ""))
                    return
                elif confirm == "A":
                    return

    @cmd2.with_category(C_MW)
    def do_currsite(self,_):
        """Get the URL of `api.php` of the current connected site"""
        self.poutput("Current site: {}".format(self.site))

    @cmd2.with_category(C_MW)
    def do_get(self,_):
        """Do a GET request"""
        req = {}
        self.poutput("Format: <key>,<value>. Use EOF to end request. Use # to comment.")
        while True:
            try:
                inp = self.read_input(prompt="> ")
            except EOFError:
                return
            if inp == "EOF": break
            if inp[0] == "#": continue
            split = inp.split(",",1)
            if len(split) == 1:
                self.poutput("# ^ INVALID")
                continue
            req[split[0]] = split[1]
        try:
            self.poutput(self.API.get(req))
        except mw.MWAPIError as e:
            self.poutput(e.dump)

    @cmd2.with_category(C_MW)
    def do_post(self,_):
        """Do a POST request"""
        req = {}
        self.poutput("Format: <key>,<value>. Use EOF to end request. Use # to comment.")
        while True:
            try:
                inp = self.read_input(prompt="> ")
            except EOFError:
                return
            if inp == "EOF": break
            if inp[0] == "#": continue
            split = inp.split(",",1)
            if len(split) == 1:
                self.poutput("> #! ^ INVALID")
                continue
            req[split[0]] = split[1]
        try:
            self.poutput(self.API.post(req))
        except mw.MWAPIError as e:
            self.poutput(e.dump)




if __name__ == '__main__':
    import sys
    site = input("Enter api.php URL or [<wmsite> <wmlang>]: ").split(" ")
    if len(site) == 1:
        try:
            siteurl = getattr(mw.WMSites,site[0])()
        except AttributeError:
            siteurl = site[0]
    else:
        try:
            siteurl = getattr(mw.WMSites,site[0])(site[1])
        except AttributeError:
            print("invalid")
            exit(1)
    c = App(siteurl)
    sys.exit(c.cmdloop())


