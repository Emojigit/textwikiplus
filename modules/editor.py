import subprocess, getpass, os, tempfile
EDITOR = "/usr/bin/nano"
ROVIEW = "/usr/bin/less"
TMPDIR = tempfile.gettempdir()+"/textwikiplus-"+str(os.getuid())+"-"+str(os.getpid())

def editor(init=""):
    with open(TMPDIR, 'w') as file:
        file.write(init)
    subprocess.Popen([EDITOR,TMPDIR]).wait()
    with open(TMPDIR, 'r') as file:
        CONT = file.read()
    with open(TMPDIR, 'w') as file:
        file.write("")
    return CONT

def dir():
    return TMPDIR

def remove():
    os.remove(TMPDIR)

def ro(content):
    with open(TMPDIR, 'w') as file:
        file.write(content)
    subprocess.Popen([ROVIEW,TMPDIR]).wait()
    with open(TMPDIR, 'w') as file:
        file.write("")
