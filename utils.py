import glob
import os


def create_file(path):
    open(path, 'w').close()


def read_file(path):
    with open(path) as f:
        res = f.read().split("\n")

    return res


def _filter(it):
    for i in it:
        if os.path.exists(i) and os.path.isfile(i):
            yield i


def get_files_recursively(path, initials=None, filter_reg_exps=None):
    if not initials:
        initials = []

    if not filter_reg_exps:
        filter_reg_exps = []

    res = set(initials).union(glob.iglob(path, recursive=True))
    for i in filter_reg_exps:
        res = res.difference(set(glob.iglob(f'**/{i}/**', recursive=True)))

    return set(_filter(res))
