from utils.diff_utils import get_diffs, restore_state
from utils.file_utils import get_files
from commands.command import Command


class Status(Command):
    _help_string = 'Writes kind of changes for different files'

    def configure(self, subparsers):
        status = subparsers.add_parser('status', help=self._help_string)
        status.set_defaults(func=self.execute)

    def execute(self, caller, args):
        last_commit = caller.branches["head"]
        before_files = restore_state(last_commit)
        indexed_files = get_files('**/*', filter_by_gitignore=True)
        diffs = get_diffs(last_commit, indexed_files)

        deleted = set()
        for i in before_files:
            if i not in indexed_files:
                deleted.add(i)

        if deleted:
            print('Deleted files:')
            for i in deleted:
                print('   ', i)
            print()

        added = set()
        for i in indexed_files:
            if i not in before_files:
                added.add(i)

        if added:
            print('Added files:')
            for i in added:
                print('   ', i)
            print()

        modified = set()
        for file, diff in diffs.items():
            if diff and file not in added and file not in deleted:
                modified.add(file)

        if modified:
            print('Modified files:')
            for i in modified:
                print('   ', i)
