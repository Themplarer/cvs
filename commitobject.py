import os
import re
from datetime import datetime


class CommitObject:
    def __init__(self, message, author, content, prev_commits):
        self.message = message
        self.author = author
        self.content = content
        self.prev_commits = prev_commits
        self.time = datetime.now()
        self.hash = (hash(frozenset(content)) + hash(message)) % (10 ** 10)

    def __str__(self):
        return f'["{self.message}" "{self.author}" "{self.hash}" ' \
               f'"{self.prev_commits if self.prev_commits else ""}"]'

    @staticmethod
    def parse(string):
        _parse_common = re.compile(r'\["(.*)" "(.*)" "(.*)" "(.*)"]')
        components = _parse_common.match(string).groups()
        commit = CommitObject(components[0],
                              components[1],
                              os.listdir('./.goodgit/commits/' + components[2]),
                              components[3].split())

        return commit
