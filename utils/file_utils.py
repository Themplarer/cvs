import glob
import os
import re

_comments = re.compile(r'^(#.*)| $')


def create_file(path):
    open(path, 'w', encoding="UTF-8").close()


def read_file(path):
    with open(path, encoding="UTF-8") as f:
        res = f.read().splitlines()

    return res


def write_file(path, lines):
    with open(path, 'w', encoding="UTF-8") as f:
        f.writelines('\n'.join(lines))


def exists(path):
    return os.path.exists(path)


def _filter(it, regexps):
    for i in it:
        i = i.replace('\\', '/')
        if os.path.exists(i) and os.path.isfile(i):
            res = True

            for j in regexps:
                if j.match(i):
                    res = False
                    break

            if res:
                yield i


def get_files(path, initials=None, filter_by_gitignore=False):
    files = set()
    if initials:
        files = set(initials)

    regexps = [] if not filter_by_gitignore else _get_gitignore_regexps()
    for i in glob.iglob(path, recursive=True):
        files.add(i)

    return set(_filter(files, regexps))


def _get_gitignore_regexps():
    ignore = set()
    for line in read_file('./.gitignore'):
        if line and not _comments.match(line):
            ignore.add(re.compile(_reformat_string(line)))

    return ignore


def _reformat_string(s):
    return '.*' + \
           s.replace('\\', '/').replace('//', '/').replace('*', '.*') + \
           '.*'
