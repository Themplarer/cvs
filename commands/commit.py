import glob
import os
import re

import utils
from argsparseerror import ArgsParseError
from commands.command import Command
from commitobject import CommitObject
from diff_finder import write_diffs
from utils import create_file, read_file


def _to_list(elem):
    return [elem] if elem else []


class Commit(Command):
    help_string = '''Usage: python ./main.py commit [message]
    message - kind of description for commit, compulsory argument
    
    Adds specified files and directories to the index'''

    def parse_args(self, args):
        if len(args) != 1:
            raise ArgsParseError
        return {'message': args[0]}

    def execute(self, caller, args):
        prev_commit = caller.branches['head']
        with open('./.goodgit/index') as f:
            indexed_files = f.read().splitlines()

        if len(indexed_files) == 0:
            print('nothing to commit!')
            return

        commit = CommitObject(args['message'], caller.author,
                              indexed_files, _to_list(prev_commit))

        path = f'{caller.dir_path}/commits/{commit.hash}'
        os.mkdir(path)
        write_diffs(prev_commit, indexed_files, path)

        with open('./.goodgit/main') as f:
            content = f.read()

        with open(path + '_info', 'w') as f:
            f.write(str(commit))

        content = re.sub(rf'{caller.selected_branch}:.*',
                         f'{caller.selected_branch}:{commit.hash}', content)
        content = re.sub(r'head:.*\n', f'head:{commit.hash}\n', content)

        with open('./.goodgit/main', 'w') as f:
            f.write(content)

        create_file('./.goodgit/index')

        print(commit.hash)
