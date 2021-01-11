#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from modules import mediawiki as mw
from modules import editor, rev
import requests, getpass
S = requests.Session()
# editor.editor

def edit(se,title):
    tdata = mw.token(se,"csrf")
    starttimestamp = tdata[1]
    token = tdata[0]
    pagedata = mw.getpage(se,title)
    pagecontent = pagedata[0]
    pageTS = pagedata[1]
    content = editor.editor(pagecontent)
    minor = False
    summary = input("Please type your edit summary: ")
    while True:
        minput = input("Do you want to mark your edit a minor edit? (Y/N) ")
        if minput == "Y" or minput == "y":
            minor = True
            break
        elif minput == "N" or minput == "n":
            minor = False
            break
        else:
            print("Please enter `Y` or `N`.")
    mw.edit(se,token,title,content,summary,False,pageTS,starttimestamp,minor)

def logout(se):
    token = mw.token(S,"csrf")[0]
    mw.logout(se,token)

def main():
    editor.create()
    print("TextWikiEdit Plus By Cato Yiu")
    print("Copyright (c) 2020 Cato Yiu")
    print("This program is under GNU GPLv3 license.")
    print("To get a list of command, use the `help` command.")
    while True:
        try:
            cmddata = input("> ").split(' ',1)
            try:
                cmd = cmddata[0]
            except IndexError:
                continue
            try:
                param = cmddata[1]
            except IndexError:
                param = ""
            if cmd == "login":
                if param == "":
                    print("Usage: login <Username>")
                    continue
                token = mw.token(S,"login")[0]
                print("Logging in as "+param)
                passwd = getpass.getpass("Plase enter your password: ")
                status = mw.login(S,token,param,passwd)
                del passwd
                if status == True:
                    print("Logged in!")
                else:
                    print("Login Failed.")
            elif cmd == "view":
                if param == "":
                    print("Usage: view <Page title>")
                    continue
                pagedata = mw.getpage(S,param)
                pagecontent = pagedata[0]
                editor.ro(pagecontent)
            elif cmd == "edit":
                if param == "":
                    print("Usage: edit <Page title>")
                    continue
                edit(S,param)
            elif cmd == "whoami":
                uinfo = mw.userinfo(S)
                if uinfo["id"] == 0:
                    print("You are IP user, the IP is "+uinfo["name"])
                else:
                    print("You are "+uinfo["name"]+", the user ID is "+str(uinfo["id"]))
            elif cmd == "logout":
                logout(S)
            elif cmd == "exit":
                logout(S)
                print("Bye")
                editor.remove()
                exit(0)
            elif cmd == "help":
                print("""List of command:
* login <Username> : Login as lgusername
* view <Title> : view article's Content
* edit <Title> : Edit an article
* whoami : know who are you
* logout : logout
* exit : Exit TextWikiPlus""")
            elif cmd == "rev":
                if param == "":
                    print("Usage: rev <Page title>")
                    continue
                editor.ro(rev.get(mw.revisions(S,param),param))
            else:
                print(cmd+": command not found")
        except KeyboardInterrupt:
            print()
            pass

if __name__ == '__main__':
    main()
