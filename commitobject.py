import re
from datetime import datetime
from pathlib import Path

from utils.file_utils import get_files

_parse_common = re.compile(r'"(.*)" "(.*)" "(.*)" "(.*)" "(.*)"')
_format = '%Y-%m-%d %H:%M:%S'


def compute_commit_hash(commit_diffs):
    res = 0
    for file, diffs in commit_diffs.items():
        res += hash(tuple(diffs))

    return res % 10 ** 10


class CommitObject:
    def __init__(self, message, author, file_names, prev_commits, commit_hash,
                 time=None):
        self.message = message
        self.author = author
        self.file_names = set(file_names)
        self.prev_commits = prev_commits if prev_commits else list()
        self.hash = commit_hash

        if not time:
            time = datetime.now()

        self.time = datetime(time.year, time.month, time.day, time.hour,
                             time.minute, time.second, 0)

    def __str__(self):
        return f'"{self.message}" "{self.author}" "{self.hash}" ' \
               f'"{self.time.strftime(_format)}" ' \
               f'"{" ".join(map(lambda c: str(c.hash), self.prev_commits))}"'

    def __eq__(self, other):
        if type(other) != type(self):
            raise ValueError('second argument is not a CommitObject!')

        return self.message == other.message and \
            self.author == other.author and self.hash == other.hash and \
            self.time == other.time and self.prev_commits == other.prev_commits

    @staticmethod
    def parse(string, get_commit_func):
        cmp = _parse_common.match(string).groups()
        commit_folder = Path('.goodgit') / 'commits' / cmp[2]
        files = get_files('*', commit_folder)
        commit = CommitObject(cmp[0],
                              cmp[1],
                              files,
                              list(map(get_commit_func, cmp[4].split())),
                              int(cmp[2]),
                              datetime.strptime(cmp[3], _format))

        return commit
