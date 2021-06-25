from io import open
from os import path
from time import sleep


def fixer(Fpath, Form):
    with open(Fpath, mode="r", encoding="cp1256") as fd:
        content = fd.read()

    if Fpath.find(Form, -1):
        Fpath = Fpath[:-4] + f'.edited{Form}'

        with open(Fpath, mode="w", encoding="utf-8") as fd:
            fd.write(content)


def Fcheck(Fpath):
    if path.isdir(Fpath):
        # print("\nIt is a directory")
        return False
    elif path.isfile(Fpath):
        # print("\nIt is a normal file")
        return True
    else:
        # print("It is a special file (socket, FIFO, device file)")
        return False


def useless(Dfile):
    for form in ['.srt', '.ass', '.SRT']:
        if Dfile.endswith(form):
            return form


def main(Flist):
    count = 0

    total = len(Flist)
    for items in Flist:
        if Fcheck(items):
            try:
                with open(items, mode="r", encoding="utf-8") as fd:
                    fd.read()
            except UnicodeDecodeError:
                count += 1
                fixer(items, useless(items))
                sleep(0.2)
    return total - count
