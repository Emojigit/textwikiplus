def get(PAGEDEF):
    status = PAGEDEF[0]
    REVS = PAGEDEF[1][0]["revisions"]
    if status == False:
        return "Page doesn't exist"
    else:
        RETSTR = ""
        for i in REVS:
            RETSTR = RETSTR + i["timestamp"] + " " + i["user"] + " (" + i["comment"] + ") Tags:"
            for t in i["tags"]:
                RETSTR = RETSTR + " " + t
        RETSTR = RETSTR + "\n"
        return RETSTR
