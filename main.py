#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from modules import mediawiki as mw
from modules import editor, rev, bsave
import requests, getpass
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

def undo(se,title,id):
    tdata = mw.token(se,"csrf")
    token = tdata[0]
    minor = False
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
    mw.undo(se,token,title,id,False,minor)

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
* exit : Exit TextWikiPlus""")
            elif cmd == "rev":
                if param == "":
                    print("Usage: rev <Page title>")
                    continue
                editor.ro(rev.get(mw.revisions(S,param),param))
            elif cmd == "rollback":
                if param == "":
                    print("Usage: rollback <Username> <Title>")
                    continue
                PARAMSplit = param.split(' ',1)
                try:
                    Uname = PARAMSplit[0]
                    Title = PARAMSplit[1]
                except KeyError:
                    print("Usage: getimage <Image Name> <Path>")
                    continue
                token = mw.token(S,"rollback")[0]
                mw.rollback(S,token,Title,Uname)
            elif cmd == "undo":
                if param == "":
                    print("Usage: undo <ID> <title>")
                    continue
                PARAMSplit = param.split(' ',1)
                try:
                    ID = PARAMSplit[0]
                    Title = PARAMSplit[1]
                except KeyError:
                    print("Usage: getimage <Image Name> <Path>")
                    continue
                try:
                    undo(S,Title,int(ID))
                except ValueError:
                    print("Usage: rev <ID> <title>")
                    pass
            elif cmd == "random":
                ns = 0
                if param == "":
                    ns = 0
                else:
                    try:
                        ns = int(param)
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
                if param == "":
                    print("Usage: getimage <Image Name> <Path>")
                    continue
                PARAMSplit = param.split(' ',1)
                try:
                    iname = PARAMSplit[0]
                    path = PARAMSplit[1]
                except KeyError:
                    print("Usage: getimage <Image Name> <Path>")
                    continue
                cont = mw.getimage(S,iname)
                if cont == False:
                    continue
                bsave.bsave(path,cont)
            elif cmd == "userinfo":
                if param == "":
                    print("Usage: Userinfo <Username>")
                    continue
                mw.userinfo(S,param)
            elif cmd == "":
                continue
            else:
                print(cmd+": command not found")
        except KeyboardInterrupt:
            print()
            pass
        except:
            editor.create()
            editor.remove()
            raise


if __name__ == '__main__':
    main()
