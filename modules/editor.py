import subprocess, getpass, os, tempfile
EDITOR, ROVIEW = "",""
if os.name == 'nt':
    EDITOR = "notepad"
    ROVIEW = "notepad"
else:
    EDITOR = "/usr/bin/nano"
    ROVIEW = "/usr/bin/less"
TMPDIR = os.path.join(tempfile.gettempdir(),"textwikiplus-"+str(getpass.getuser())+"-"+str(os.getpid())+".txt")

def editor(init=""):
    with open(TMPDIR, 'w', encoding="utf-8") as file:
        file.write(init)
    subprocess.Popen([EDITOR,TMPDIR]).wait()
    with open(TMPDIR, 'r', encoding="utf-8") as file:
        CONT = file.read()
    with open(TMPDIR, 'w', encoding="utf-8") as file:
        file.write("")
    return CONT

def dir():
    return TMPDIR

def remove():
    os.remove(TMPDIR)

def ro(content):
    with open(TMPDIR, 'w', encoding="utf-8") as file:
        file.write(content)
    subprocess.Popen([ROVIEW,TMPDIR]).wait()
    with open(TMPDIR, 'w', encoding="utf-8") as file:
        file.write("")

def create():
    with open(TMPDIR, 'w', encoding="utf-8") as file:
        file.write("")
