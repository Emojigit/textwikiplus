def get(PAGEDEF, title):
    status = PAGEDEF[0]
    if status == False:
        return "Page `"+title+"` doesn't exist"
    else:
        REVS = PAGEDEF[1][0]["revisions"]
        RETSTR = "The history of `"+title+"`"
        for i in REVS:
            RETSTR = RETSTR + "\n"
            RETSTR = RETSTR + i["timestamp"] + " ID:" + str(i["revid"]) + " " + i["user"] + " (" + i["comment"] + ") Tags:"
            for t in i["tags"]:
                RETSTR = RETSTR + " " + t
        return RETSTR
