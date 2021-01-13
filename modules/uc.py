def get(PAGEDEF, uname):
    status = PAGEDEF[0]
    if status == False:
        return "Error while loading contribs"
    else:
        RETSTR = "The user contribs of `"+uname+"`"
        for i in PAGEDEF[1]:
            RETSTR = RETSTR + "\n"
            RETSTR = RETSTR + i["title"] + " " + i["timestamp"] + " (" + i["comment"] + ")"
        return RETSTR
