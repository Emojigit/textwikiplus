def bsave(path,content):
    with open(path, 'wb+') as outfile:
        outfile.write(content)
