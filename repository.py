import getpass
import pathlib
import re

from commitobject import CommitObject


class Repository:
    _branch = re.compile(r'^(.*):(.*)')
    _selected_branch = re.compile(r'(.*?)\|')
    author = getpass.getuser()
    dir_path = pathlib.Path('.goodgit')
    main_file_path = dir_path / 'main'
    selected_branch = 'master'
    branches = dict()

    def __init__(self):
        if self.is_initiated:
            self._fill_branches()

    @property
    def is_initiated(self):
        return self.dir_path.exists() and self.main_file_path.exists()

    def get_commit(self, commit_hash):
        if not commit_hash:
            return None

        with open(f'{self.dir_path}/commits/{commit_hash}_info') as f:
            s = f.readline()

        return CommitObject.parse(s, self)

    def _fill_branches(self):
        with open(self.main_file_path) as f:
            for line in f:
                match = self._branch.match(line)
                if match:
                    self.branches[match.group(1)] = None
                    if len(match.groups()) == 2:
                        self.branches[match.group(1)] = self.get_commit(
                            match.group(2))
                else:
                    match = self._selected_branch.match(line)

                    if match:
                        self.selected_branch = match.group(1)
