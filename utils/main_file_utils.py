import pathlib
import re

from commitobject import CommitObject
from utils.file_utils import write_file

_sep = '__________'
_branch = re.compile(r'^(.*):(.*)')
_selected_branch = re.compile(r'(.*?)\|')


def write_main_file(selected_branch, branches, tags, base_path=None):
    if not base_path:
        base_path = pathlib.Path('.')

    lines = ['KHOROSHiy_git v.1.0', _sep, selected_branch + '|', _sep]
    for branch, commit in branches.items():
        commit_hash_str = str(commit.hash) if commit else ''
        lines.append(f'{branch}:{commit_hash_str}')

    if tags:
        lines.append(_sep)

        for tag, commit in tags.items():
            commit_hash_str = str(commit.hash) if commit else ''
            lines.append(f'{tag}:{commit_hash_str}')

    write_file(base_path / '.goodgit/main', lines)


def _get_commit(commit_hash, base_path=pathlib.Path('.')):
    if not commit_hash:
        return None

    with open(base_path / '.goodgit' / 'commits' / f'{commit_hash}_info') as f:
        s = f.readline()

    return CommitObject.parse(s, _get_commit)


def read_main_file(base_path=None):
    branches = dict()
    tags = dict()
    sep_counter = 0

    if not base_path:
        base_path = pathlib.Path('.')

    main_file_path = base_path / '.goodgit' / 'main'
    with main_file_path.open(encoding='UTF-8') as f:
        for line in f:
            if line.startswith(_sep):
                sep_counter += 1

            match = _branch.match(line)
            if match:
                category = branches
                if sep_counter > 2:
                    category = tags

                category[match.group(1)] = None
                if len(match.groups()) == 2:
                    category[match.group(1)] = _get_commit(match.group(2))
            else:
                match = _selected_branch.match(line)

                if match:
                    selected_branch = match.group(1)

    return selected_branch, branches, tags
