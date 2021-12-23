from commands.command import Command
from utils.diff_utils import restore_state, get_diffs


class Diff(Command):
    _help_string = 'Finds diff between two commits'

    def configure(self, subparsers):
        diff = subparsers.add_parser('diff', help=self._help_string)
        diff.set_defaults(func=self.execute)
        diff.add_argument('before', help='hash of first commit')
        diff.add_argument('after', help='hash of second commit')

    def execute(self, repository, args):
        before_files = restore_state(repository.commits[args.before])
        after_files = restore_state(repository.commits[args.after])
        diffs = get_diffs(before_files, after_files)

        if not any(diffs.values()):
            print('there is no changes!')
            return

        for file, diff in diffs.items():
            if diff:
                print(file)
                for i in diff:
                    print(i)

                print()
