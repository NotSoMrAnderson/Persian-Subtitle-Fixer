import io
import os
import time


def fixer(Fpath, Form):
    with io.open(Fpath, mode="r", encoding="cp1256") as fd:
        content = fd.read()

    if Fpath.find(Form, -1):
        Fpath = Fpath[:-4] + f'.edited{Form}'

        with io.open(Fpath, mode="w", encoding="utf-8") as fd:
            fd.write(content)


def Fcheck(Fpath):
    if os.path.isdir(Fpath):
        # print("\nIt is a directory")
        return False
    elif os.path.isfile(Fpath):
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
                with io.open(items, mode="r", encoding="utf-8") as fd:
                    fd.read()
            except Exception:
                count += 1
                fixer(items, useless(items))
                time.sleep(0.2)
    return total - count
