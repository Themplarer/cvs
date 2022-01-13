from collections import defaultdict

from utils.diff_utils import get_diffs, restore_state
from utils.file_utils import get_files, read_file
from commands.command import RepositoryDependentCommand


class Status(RepositoryDependentCommand):
    _help_string = 'Writes kind of changes for different files'

    def configure(self, subparsers):
        status = subparsers.add_parser('status', help=self._help_string)
        status.set_defaults(obj=self)

    def execute(self, repository, args, writer):
        super().execute(repository, args, writer)

        last_commit = repository.branches['head']
        before_files = restore_state(last_commit)
        indexed_files = get_files('*', filter_by_gitignore=True)
        files_after = defaultdict()

        for i in indexed_files:
            files_after[i] = list(read_file(i))

        diffs = get_diffs(before_files, files_after)
        printed_header = False
        used = set()

        for i in before_files:
            if i not in indexed_files:
                if not printed_header:
                    writer.write('Deleted files:')
                    printed_header = True
                used.add(i)
                writer.write('   ', i)

        if printed_header:
            writer.write()

        printed_header = False
        for i in indexed_files:
            if i not in before_files:
                if not printed_header:
                    writer.write('Added files:')
                    printed_header = True
                used.add(i)
                writer.write('   ', i)

        if printed_header:
            writer.write()

        for file, diff in diffs.items():
            if diff and file not in used:
                if not printed_header:
                    writer.write('Modified files:')
                    printed_header = True

                writer.write('   ', file)
