from commands.command import RepositoryDependentCommand
from utils.diff_utils import restore_state, get_diffs


class Diff(RepositoryDependentCommand):
    _help_string = 'Finds diff between two commits'

    def configure(self, subparsers):
        diff = subparsers.add_parser('diff', help=self._help_string)
        diff.set_defaults(obj=self)
        diff.add_argument('before', help='hash of first commit')
        diff.add_argument('after', help='hash of second commit')

    def execute(self, repository, args, writer):
        super().execute(repository, args, writer)

        before_files = restore_state(repository.commits[args.before])
        after_files = restore_state(repository.commits[args.after])
        diffs = get_diffs(before_files, after_files)

        if not any(diffs.values()):
            writer.write('there is no changes!')
            return

        for file, diff in diffs.items():
            if diff:
                writer.write(file)
                for i in diff:
                    writer.write(i)

                writer.write()
