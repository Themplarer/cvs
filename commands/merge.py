from commands.command import RepositoryDependentCommand
from commitobject import CommitObject, compute_commit_hash
from utils.diff_utils import restore_state, get_diffs, write_diffs


class Merge(RepositoryDependentCommand):
    _help_string = 'Merges specified branch into head'

    def configure(self, subparsers):
        merge = subparsers.add_parser('merge', help=self._help_string)
        merge.set_defaults(obj=self)
        merge.add_argument('branch', help='name of branch')

    def execute(self, repository, args, writer):
        super().execute(repository, args, writer)

        branch = args.branch
        if repository.selected_branch == branch:
            writer.write('It\'s impossible to merge branch with itself!')
            return

        head = repository.branches['head']
        second = repository.branches[branch]

        if head == second:
            writer.write('Nothing to merge!')
            return

        diffs = get_diffs(restore_state(head), restore_state(second))
        commit = CommitObject(
            f'merge {branch} into {repository.selected_branch}',
            repository.author, diffs.keys(), [head, second],
            compute_commit_hash(diffs))

        path = repository.dir_path / 'commits' / str(commit.hash)
        path.mkdir()
        write_diffs(diffs, path)

        with open(str(path) + '_info', 'w') as f:
            f.write(str(commit))

        repository.branches[repository.selected_branch] = commit
        repository.branches['head'] = commit

        writer.write(commit.hash)
