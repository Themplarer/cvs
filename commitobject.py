import re
from datetime import datetime

from utils.file_utils import get_files

_parse_common = re.compile(r'\["(.*)" "(.*)" "(.*)" "(.*)"]')


def _get_commit_hashes_str(commits):
    return " ".join(map(lambda c: str(c.hash), commits))


class CommitObject:
    def __init__(self, message, author, file_names, prev_commits,
                 commit_hash=None):
        self.message = message
        self.author = author
        self.file_names = set(file_names)
        self.prev_commits = prev_commits if prev_commits else list()
        self.time = datetime.now()
        self.hash = commit_hash
        if not commit_hash:
            self.hash = (hash(frozenset(file_names)) + hash(message)) \
                        % (10 ** 10)

    def __str__(self):
        return f'["{self.message}" "{self.author}" "{self.hash}" ' \
               f'"{_get_commit_hashes_str(self.prev_commits)}"]'

    @staticmethod
    def parse(string, caller):
        cmp = _parse_common.match(string).groups()
        commit_folder = f'./.goodgit/commits/{cmp[2]}/'
        files = map(lambda x: x.replace(commit_folder, ''),
                    get_files(f'{commit_folder}**'))
        commit = CommitObject(cmp[0],
                              cmp[1],
                              files,
                              list(map(caller.get_commit, cmp[3].split())),
                              cmp[2])

        return commit
