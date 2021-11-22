import os
import re

from commands.command import Command
from commitobject import CommitObject
from diff_utils import write_diffs
from utils import create_file, read_file


class Commit(Command):
    _help_string = 'Commits files from index to the current branch'

    def configure(self, subparsers):
        commit = subparsers.add_parser('commit', help=self._help_string)
        commit.set_defaults(func=self.execute)
        commit.add_argument('-m', '--message', help='description for commit')

    def execute(self, caller, args):
        prev_commit = caller.branches['head']

        indexed_files = read_file('./.goodgit/index')
        if len(indexed_files) == 0:
            print('nothing to commit!')
            return

        commit = CommitObject(args.message, caller.author, indexed_files,
                              [prev_commit] if prev_commit else [])

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
