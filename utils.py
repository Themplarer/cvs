import glob
import os


def create_file(path):
    open(path, 'w').close()


def read_file(path):
    with open(path) as f:
        res = f.read().split("\n")

    return res


def _filter(it, filter_reg_exps):
    for i in it:
        if os.path.exists(i) and os.path.isfile(i):
            res = False
            for j in filter_reg_exps:
                res = res or j.match(i)

            if not res:
                yield i


def get_files_recursively(initials, path, filter_reg_exps=None):
    if not filter_reg_exps:
        filter_reg_exps = []

    yield from _filter(initials, filter_reg_exps)
    yield from _filter(glob.iglob(path + '/**', recursive=True),
                       filter_reg_exps)
