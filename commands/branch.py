from commands.command import RepositoryDependentCommand


class Branch(RepositoryDependentCommand):
    _protected_branches = {'head', 'master'}
    _help_string = 'Does something to some branch. ' \
                   'Default - shows list of all branches'

    def configure(self, subparsers):
        branch = subparsers.add_parser('branch', help=self._help_string)
        branch.set_defaults(obj=self)
        branch.add_argument('branch', help='branch name', nargs='?')
        branch.add_argument('-d', action='store_true',
                            help='deletes the branch')

    def execute(self, repository, args, writer):
        super().execute(repository, args, writer)

        if not args.branch:
            if args.d:
                writer.write('called to delete a branch but branch is not '
                             'specified')
                return

            for i in repository.branches.keys():
                writer.write(i)
            return

        branch = args.branch
        if args.d:
            if branch in self._protected_branches:
                writer.write('it\'s impossible to delete protected branch!')
                return

            if branch in repository.branches:
                repository.branches.pop(branch)
                writer.write('deleted!')
            else:
                writer.write('there is no such branch!')

            return

        if branch in repository.branches:
            writer.write('this branch has already existed!')
            return

        repository.branches[branch] = repository.branches['head']
        writer.write('branched!')
