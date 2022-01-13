import re
from collections import defaultdict
from difflib import unified_diff
from pathlib import Path

from utils.file_utils import read_file, get_files, write_file

_path_regexp = re.compile(r'.*/commits/\d*[/\\](.*)')
_lines_regexp = re.compile(r'@@ -(\d+)(,(\d*))? \+.* @@')


def write_diffs(diffs_dict, result_dir):
    """Writes diffs of files to the result_dir"""
    for file, diff in diffs_dict.items():
        if diff:
            file = result_dir / file
            file.parent.mkdir(parents=True, exist_ok=True)
            write_file(file, diff)


def get_diffs(files_before, files_after):
    """Returns dictionary of all diffs between two states of files"""
    for file in set(files_before.keys()).union(files_after.keys()):
        diff = _remove_endlines(unified_diff(files_before[file],
                                             files_after[file]))
        files_before[file] = list(diff)

    return files_before


def restore_state(commit):
    """Returns state of all files at the moment of the commit"""
    res = defaultdict(lambda: [])

    if commit:
        if commit.prev_commits:
            res = restore_state(commit.prev_commits[0])

        commits_folder = Path('.goodgit') / 'commits'
        for i in get_files('*', commits_folder / str(commit.hash)):
            path = Path(_path_regexp.match(i.as_posix()).group(1))
            res[path] = merge_file(res[path], list(read_file(i)))

    return res


def merge_file(file, diff):
    """Applies diff to the file"""
    new_file = []
    line_pointer = 1

    for i in diff:
        if i != '--- ' and i != '+++ ':
            match = _lines_regexp.match(i)

            if match:
                left_border = int(match.group(1))
                right_border = len(file) + 1
                if match.group(3):
                    right_border = int(match.group(3)) + left_border
                for j in range(line_pointer, left_border):
                    new_file.append(file[j - 1])
                line_pointer = max(line_pointer, right_border)
            else:
                line = i
                if len(i) == 0 or i[0] != '-':
                    if len(i) > 0:
                        line = line[1:]

                    new_file.append(line)

    for i in range(line_pointer, len(file) + 1):
        new_file.append(file[i - 1])

    return new_file


def _remove_endlines(array):
    for i in array:
        yield i.strip('\n')
