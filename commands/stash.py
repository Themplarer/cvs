from collections import defaultdict
from pathlib import Path

from commands.command import Command
from utils.diff_utils import get_diffs, write_diffs, restore_state
from utils.file_utils import get_files, read_file


class Stash(Command):
    _help_string = 'Stashes all uncommitted changes'

    def configure(self, subparsers):
        stash = subparsers.add_parser('stash', help=self._help_string)
        stash.set_defaults(func=self.execute)

    def execute(self, repository, args):
        commit = repository.branches['head']

        if not commit:
            print('impossible to stash anything since there is no commits!')
            return

        # stashes_path = Path('.goodgit') / 'stashes'
        # stashes_count = len(list(stashes_path.iterdir()))
        # indexed_files = get_files('*', filter_by_gitignore=True)
        # files_after = defaultdict()
        # for p in indexed_files:
        #     files_after[p] = read_file(p)
        #
        # diffs = get_diffs(restore_state(commit), files_after)
        # write_diffs(diffs, stashes_path / str(stashes_count + 1))

        print('WORK IN PROGRESS')
