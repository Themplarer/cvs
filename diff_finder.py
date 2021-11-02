import os
import re
from collections import defaultdict
from difflib import unified_diff

import utils
from utils import read_file

_path_regexp = re.compile(r'.*/commits/\d*[/\\](.*)')
_lines_regexp = re.compile(r'@@ -(\d+),(\d+) \+.* @@')


def _remove_endlines(array):
    for i in array:
        yield i.strip('\n')


def write_diffs(last_commit, files_after, result_dir):
    files_before_dict = defaultdict(lambda: [])
    if last_commit:
        files_before_dict = restore_state(last_commit)

    for file in files_after:
        before = files_before_dict[file] if file in files_before_dict else []
        after = read_file(file)
        diff = _remove_endlines(unified_diff(before, after))
        lines = '\n'.join(diff)

        if lines:
            file = result_dir + '/' + file
            if '/' in file:
                os.makedirs(os.path.dirname(file), exist_ok=True)

            with open(file, 'w') as f:
                f.writelines(lines)


def restore_state(commit):
    if not commit:
        return []

    res = defaultdict(lambda: [])
    if commit.prev_commits:
        res = restore_state(commit.prev_commits[0])

    for i in utils.get_files_recursively([],
                                         f'./.goodgit/commits/{commit.hash}'):
        path = _path_regexp.match(i).group(1)
        res[path] = merge_file(res[path], read_file(i))
    return res


def merge_file(file, diff):
    new_file = []
    line_pointer = 1

    for i in diff:
        if i != '--- ' and i != '+++ ':
            match = _lines_regexp.match(i)

            if match:
                left_border = int(match.group(1))
                right_border = int(match.group(2)) + left_border
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
