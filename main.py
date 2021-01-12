#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from modules import mediawiki as mw
from modules import editor, rev, bsave
import requests, getpass
from modules.err import ParamError
S = requests.Session()

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

def emailuser(se,uname):
    tdata = mw.token(se,"csrf")
    token = tdata[0]
    title = input("Email subject: ")
    content = editor.editor("")
    mw.emailuser(se,token,uname,title,content)

def undo(se,title,id):
    tdata = mw.token(se,"csrf")
    token = tdata[0]
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
    mw.undo(se,token,title,id,False,minor,summary)

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
                paramm = param.rstrip()
                token = mw.token(S,"login")[0]
                print("Logging in as "+paramm)
                passwd = getpass.getpass("Plase enter your password: ")
                status = mw.login(S,token,paramm,passwd)
                del passwd
                if status == True:
                    print("Logged in!")
                else:
                    print("Login Failed.")
            elif cmd == "view":
                if param == "":
                    print("Usage: view <Page title>")
                    continue
                pagedata = mw.getpage(S,param.rstrip())
                pagecontent = pagedata[0]
                editor.ro(pagecontent)
            elif cmd == "edit":
                if param == "":
                    print("Usage: edit <Page title>")
                    continue
                edit(S,param)
            elif cmd == "whoami":
                uinfo = mw.whoami(S)
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
* rev <Title> : Get page history
* rollback <Username> <title> : Rollback edit by Username in a page
* undo <ID> <title> : Undo edit with ID <ID> in page <title>
* random [NS ID] : Get random page title in [NS ID] or main namespace
* clear : clear the screen
* nsinfo : Get wiki's namespaces infomation
* wikiinfo : Get wiki's general infomations
* exinfo : Get wii's extensions infomation
* getimage <File name> <Local dir> : Download a remote image
* userinfo <Username> : get user info
* emailuser : Email a user
* debug <bool> : change debug setting
* exit : Exit TextWikiPlus""")
            elif cmd == "rev":
                if param == "":
                    print("Usage: rev <Page title>")
                    continue
                editor.ro(rev.get(mw.revisions(S,param.rstrip()),param.rstrip()))
            elif cmd == "rollback":
                if param == "":
                    print("Usage: rollback <Username> <Title>")
                    continue
                PARAMSplit = param.split(' ',1)
                try:
                    Uname = PARAMSplit[0]
                    Title = PARAMSplit[1].rstrip()
                except KeyError:
                    print("Usage: getimage <Image Name> <Path>")
                    continue
                token = mw.token(S,"rollback")[0]
                mw.rollback(S,token,Title,Uname)
            elif cmd == "undo":
                try:
                    if param == "":
                        raise ParamError
                    PARAMSplit = param.split(' ',1)
                    try:
                        ID = PARAMSplit[0]
                        Title = PARAMSplit[1].rstrip()
                    except KeyError:
                        raise ParamError
                    try:
                        undo(S,Title,int(ID.rstrip()))
                    except ValueError:
                        raise ParamError
                except ParamError:
                    print("Usage: undo <ID> <Title>")
                    pass
            elif cmd == "random":
                ns = 0
                if param == "":
                    ns = 0
                else:
                    try:
                        ns = int(param.rstrip())
                    except ValueError:
                        print("Param must be None or int!")
                        continue
                mw.random(S,ns)
            elif cmd == "clear":
                print(chr(27) + "[2J")
            elif cmd == "nsinfo":
                mw.nsinfo(S)
            elif cmd == "wikiinfo":
                print(mw.wikiinfo(S))
            elif cmd == "exinfo":
                editor.ro(mw.exinfo(S))
            elif cmd == "getimage":
                try:
                    if param == "":
                        raise ParamError
                    PARAMSplit = param.split(' ',1)
                    try:
                        iname = PARAMSplit[0].rstrip()
                        path = PARAMSplit[1].rstrip()
                    except KeyError:
                        raise ParamError
                    cont = mw.getimage(S,iname)
                    if cont == False:
                        continue
                        bsave.bsave(path,cont)
                except ParamError:
                    print("Usage: getimage <Image Name> <Path>")
                    pass
            elif cmd == "userinfo":
                if param == "":
                    print("Usage: Userinfo <Username>")
                    continue
                mw.userinfo(S,param.rstrip())
            elif cmd == "euser" or cmd == "emailuser":
                if param == "":
                    print("Usage: emailuser <Username>")
                    continue
                emailuser(S,param.rstrip())
            elif cmd == "debug":
                if param == "True" or param == "true" or param == "1":
                    mw.setdebug(True)
                elif param == "False" or param == "false" or param == "0":
                    mw.setdebug(False)
                else:
                    print("current debug state: "+str(mw.setdebug()))

            elif cmd == "":
                continue
            else:
                print(cmd+": command not found")
        except KeyboardInterrupt:
            print()
            pass
        except:
            print()
            print("[ERROR] an error raised! You can report it at https://github.com/Emojigit/textwikiplus")
            editor.remove()
            raise


if __name__ == '__main__':
    main()
