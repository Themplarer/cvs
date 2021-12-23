from commands.command import Command


class Branch(Command):
    _protected_branches = {'head', 'master'}
    _help_string = 'Does something to some branch. ' \
                   'Default - shows list of all branches'

    def configure(self, subparsers):
        branch = subparsers.add_parser('branch', help=self._help_string)
        branch.set_defaults(func=self.execute)
        branch.add_argument('branch', help='branch name', nargs='?')
        branch.add_argument('-d', action='store_true',
                            help='deletes the branch')

    def execute(self, repository, args):
        if not args.branch:
            for i in repository.branches.keys():
                print(i)

            return

        branch = args.branch
        if args.d:
            if branch in self._protected_branches:
                print('it\'s impossible to delete protected branch!')
                return

            if branch in repository.branches:
                repository.branches.pop(branch)
                print('deleted!')
            else:
                print('there is no such branch!')

            return

        if branch in repository.branches:
            print('this branch has already existed!')
            return

        head_commit = repository.branches['head']
        repository.branches[branch] = head_commit
        print('branched!')
