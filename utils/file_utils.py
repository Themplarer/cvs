import re
from pathlib import Path

_comments = re.compile(r'^(#.*)| $')
_slash_regexp = re.compile(r'[/\\]+')


def read_file(path):
    """Reads file contents line by line. Returns iterator of splitted lines
    with no \\n"""
    with path.open(encoding='UTF-8') as f:
        for i in f:
            yield i.replace('\n', '')


def write_file(path, lines):
    """Writes file contents line by line separated by new line"""
    with path.open(encoding='UTF-8', mode='w') as f:
        is_first_line = True
        lines_iter = iter(lines)

        try:
            while True:
                line = next(lines_iter)
                if not is_first_line:
                    f.write('\n')

                is_first_line = False
                f.write(line)
        except StopIteration:
            pass


def get_files(mask, path='.', initials=None, filter_by_gitignore=False):
    """Returns set of files located in the directory recursively.
    May append them to the initials and filter by gitignore"""
    regexps = [] if not filter_by_gitignore else _get_gitignore_regexps()
    files = set(initials if initials else []) | set(Path(path).rglob(mask))
    return set(_filter(files, regexps))


def remove_dir_recursively(path, ok_not_exists=False):
    """Removes everything (dirs/files) starting from path"""
    if not path.exists() and ok_not_exists:
        return

    for child in path.rglob('*'):
        if child.is_file():
            child.unlink()
        else:
            remove_dir_recursively(child)
    path.rmdir()


def _filter(it, regexps):
    for i in it:
        if i.exists() and i.is_file():
            file_str = i.as_posix()
            if not any((j.match(file_str) for j in regexps)):
                yield i


def _get_gitignore_regexps():
    ignore = set()
    for line in read_file(Path('.gitignore')):
        if line and not _comments.match(line):
            ignore.add(re.compile(_reformat_string(line)))

    return ignore


def _reformat_string(s):
    return _slash_regexp.sub('/', s).replace('.', r'\.').replace('*', '.*') + \
           '.*'
