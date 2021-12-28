import getpass
import pathlib
from collections import deque

from utils.main_file_utils import write_main_file, read_main_file


class Repository:
    author = getpass.getuser()

    def __init__(self, base_path='.'):
        self.base_path = pathlib.Path(base_path)
        self.dir_path = self.base_path / '.goodgit'
        self.main_file_path = self.dir_path / 'main'

        if self.is_initiated:
            self.selected_branch, self.branches, self.tags = read_main_file()
            self.is_selected_branch = self.selected_branch in self.branches
            q = deque(self.branches.values())
            q.extend(self.tags.values())
            self.commits = self._get_commits(q)

    @property
    def is_initiated(self):
        return self.dir_path.exists() and self.main_file_path.exists()

    def save_main_file(self):
        write_main_file(self.selected_branch, self.branches, self.tags)

    @staticmethod
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
