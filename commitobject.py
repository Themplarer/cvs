import pathlib
import re
from datetime import datetime

from utils.file_utils import get_files

_parse_common = re.compile(r'"(.*)" "(.*)" "(.*)" "(.*)" "(.*)"')
_format = '%Y-%m-%d %H:%M:%S'


def compute_commit_hash(commit_diffs):
    res = 0
    for file, diffs in commit_diffs.items():
        res += hash(tuple(diffs))

    return res % 10 ** 10


def _get_commit_hashes_str(commits):
    return ' '.join(map(lambda c: str(c.hash), commits))


class CommitObject:
    def __init__(self, message, author, file_names, prev_commits, commit_hash,
                 time=None):
        self.message = message
        self.author = author
        self.file_names = set(file_names)
        self.prev_commits = prev_commits if prev_commits else list()
        self.hash = commit_hash
        self.time = time if time else datetime.now()

    def __str__(self):
        return f'"{self.message}" "{self.author}" "{self.hash}" ' \
               f'"{self.time.strftime(_format)}" ' \
               f'"{_get_commit_hashes_str(self.prev_commits)}"'

    @staticmethod
    def parse(string, repository):
        cmp = _parse_common.match(string).groups()
        commit_folder = pathlib.Path(f'./.goodgit/commits/{cmp[2]}')
        files = get_files('*', commit_folder)
        commit = CommitObject(cmp[0],
                              cmp[1],
                              files,
                              list(map(repository.get_commit, cmp[4].split())),
                              cmp[2],
                              datetime.strptime(cmp[3], _format))

        return commit
