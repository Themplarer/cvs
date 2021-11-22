import glob
import os


def create_file(path):
    open(path, 'w').close()


def read_file(path):
    with open(path) as f:
        # encoding = "UTF-8"
        res = f.read().splitlines()

    return res


def write_file(path, lines):
    with open(path, 'w') as f:
        f.writelines('\n'.join(lines))


def exists(path):
    return os.path.exists(path)


def _filter(it, regexps):
    for i in it:
        if os.path.exists(i) and os.path.isfile(i):
            res = True

            for j in regexps:
                if j.match(i.replace('\\', '/')):
                    res = False
                    break

            if res:
                yield i


def get_files(path, initials=None, regexps=None):
    if not initials:
        initials = []

    if not regexps:
        regexps = []

    return set(_filter(set(initials).union(glob.iglob(path, recursive=True)),
                       regexps))
