import os
import re
import shutil

from argsparseerror import ArgsParseError
from commands.command import Command
from commitobject import CommitObject


class Commit(Command):
    help_string = '''Usage: python ./main.py commit [message]
    message - kind of description for commit, compulsory argument
    
    Adds specified files and directories to the index'''

    def parse_args(self, args):
        if len(args) != 1:
            raise ArgsParseError
        return {'message': i for i in args}

    def execute(self, caller, args):
        prev_commit_str = caller.branches['head']
        prev_commit = CommitObject.parse(prev_commit_str)\
            if prev_commit_str else None
        # changed_files = list()
        with open('./.goodgit/index') as f:
            indexed_files = f.read().splitlines()

        commit = CommitObject(args['message'], caller.author,
                              indexed_files, prev_commit)

        path = f'{caller.dir_path}commits/{commit.hash}'
        os.mkdir(path)
        for i in indexed_files:
            dest = f'{path}/{i}'
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            shutil.copy2(i, dest)

        with open('./.goodgit/main') as f:
            content = f.read()

        content = re.sub(r'head:.*\n', f'head:{commit.hash}\n', content)

        with open('./.goodgit/main', 'w') as f:
            f.write(content)

        open('./.goodgit/index', 'w').close()

        print(commit.hash)
