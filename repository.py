import getpass
import pathlib
from collections import deque

from utils.main_file_utils import write_main_file, read_main_file


def _get_commits(q):
    commits = dict()

    while len(q):
        commit = q.popleft()
        if not commit:
            continue

        _hash = str(commit.hash)
        while commit and _hash not in commits:
            commits[_hash] = commit
            q.extend(commit.prev_commits)

    return commits


class Repository:
    """Represents goodgit repo"""
    author = getpass.getuser()
    selected_branch = 'master'
    branches = {selected_branch: None, 'head': None}
    tags = dict()

    def __init__(self):
        self.dir_path = pathlib.Path('.goodgit')
        self.main_file_path = self.dir_path / 'main'

        if self.is_initiated:
            self.selected_branch, self.branches, self.tags = read_main_file()
            q = deque(self.branches.values())
            q.extend(self.tags.values())
            self.commits = _get_commits(q)

    @property
    def is_initiated(self):
        return self.dir_path.exists() and self.main_file_path.exists()

    @property
    def is_selected_branch(self):
        return self.selected_branch in self.branches

    def save_main_file(self):
        write_main_file(self.selected_branch, self.branches, self.tags)
