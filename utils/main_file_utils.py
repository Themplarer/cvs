import re
from pathlib import Path

from commitobject import CommitObject
from utils.file_utils import write_file, read_file

_sep = '__________'
_branch = re.compile(r'^(.*):(.*)')
_selected_branch = re.compile(r'(.*?)\|')

_dir_path = Path('.goodgit')


def write_main_file(selected_branch, branches, tags):
    """Writes goodgit internal info to the main-file"""
    if selected_branch not in branches:
        raise AttributeError('bad selected branch!')

    lines = ['KHOROSHiy_git v.1.0', _sep, selected_branch + '|', _sep]
    for branch, commit in branches.items():
        commit_hash_str = str(commit.hash) if commit else ''
        lines.append(f'{branch}:{commit_hash_str}')

    if tags:
        lines.append(_sep)

        for tag, commit in tags.items():
            lines.append(f'{tag}:{commit.hash}')

    write_file(_dir_path / 'main', lines)


def read_main_file():
    """Reads goodgit internal info from main-file"""
    selected_branch = 'master'
    branches = dict()
    tags = dict()
    sep_counter = 0
    category = branches

    main_file_path = _dir_path / 'main'
    for line in read_file(main_file_path):
        if line == _sep:
            sep_counter += 1
            if sep_counter > 2:
                category = tags
            continue

        match = _branch.match(line)
        if match:
            commit = None
            if len(match.groups()) == 2:
                commit = _get_commit(match.group(2))

            category[match.group(1)] = commit
        else:
            match = _selected_branch.match(line)
            if match:
                selected_branch = match.group(1)

    return selected_branch, branches, tags


def _get_commit(commit_hash):
    if not commit_hash:
        return None

    s = next(read_file(_dir_path / 'commits' / f'{commit_hash}_info'))
    return CommitObject.parse(s, _get_commit)
