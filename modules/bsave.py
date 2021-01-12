def bsave(path,content):
    with open(path, 'wb+') as outfile:
        outfile.write(content)

def tsave(path,text):
    with open(path, 'w+') as outfile:
        outfile.write(content)
