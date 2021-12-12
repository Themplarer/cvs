import pathlib
import re

_comments = re.compile(r'^(#.*)| $')


def read_file(path):
    return path.read_text(encoding='UTF-8').splitlines()


def write_file(path, lines):
    path.write_text('\n'.join(lines), encoding='UTF-8')


def _filter(it, regexps):
    for i in it:
        if i.exists() and i.is_file():
            res = True

            file_str = i.as_posix()
            for j in regexps:
                if j.match(file_str):
                    res = False
                    break

            if res:
                yield i


def get_files(mask, path='.', initials=None, filter_by_gitignore=False):
    regexps = [] if not filter_by_gitignore else _get_gitignore_regexps()
    files = set(initials if initials else []) | \
        set(pathlib.Path(path).rglob(mask))
    return set(_filter(files, regexps))


def _get_gitignore_regexps():
    ignore = set()
    for line in read_file(pathlib.Path('.gitignore')):
        if line and not _comments.match(line):
            ignore.add(re.compile(_reformat_string(line)))

    return ignore


def _reformat_string(s):
    return s.replace('\\', '/').replace('//', '/').replace('*', '.*') + '.*'
