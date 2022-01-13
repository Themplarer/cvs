from collections import defaultdict
from pathlib import Path

from commands.command import Command
from commitobject import CommitObject, compute_commit_hash
from utils.diff_utils import write_diffs, get_diffs, restore_state
from utils.file_utils import read_file


class Commit(Command):
    _help_string = 'Commits files from index to the current branch'

    def configure(self, subparsers):
        commit = subparsers.add_parser('commit', help=self._help_string)
        commit.set_defaults(obj=self)
        commit.add_argument('-m', '--message', help='description for commit')

    def execute(self, repository, args, writer):
        super().execute(repository, args, writer)

        if not repository.is_selected_branch:
            writer.write('it\'s impossible to commit to this pointer! '
                         'checkout branch before')

        prev_commit = repository.branches['head']
        indexed_files = list()
        files_after = defaultdict()
        for i in read_file(repository.dir_path / 'index'):
            p = Path(i)
            indexed_files.append(p)
            files_after[p] = list(read_file(p))

        diffs = get_diffs(restore_state(prev_commit), files_after)
        if len(indexed_files) == 0 or not any(diffs.values()):
            writer.write('nothing to commit!')
            return

        commit = CommitObject(args.message, repository.author, indexed_files,
                              [prev_commit] if prev_commit else [],
                              compute_commit_hash(diffs))

        path = repository.dir_path / 'commits' / str(commit.hash)
        path.mkdir()
        write_diffs(diffs, path)

        with open(str(path) + '_info', 'w') as f:
            f.write(str(commit))

        repository.branches[repository.selected_branch] = commit
        repository.branches['head'] = commit

        Path('.goodgit/index').write_text('')
        writer.write(commit.hash)
