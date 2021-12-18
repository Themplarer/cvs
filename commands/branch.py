from commands.command import Command


class Branch(Command):
    _help_string = 'Does something to some branch. ' \
                   'Default - creates a new based on head'

    def configure(self, subparsers):
        branch = subparsers.add_parser('branch', help=self._help_string)
        branch.set_defaults(func=self.execute)
        branch.add_argument('branch', help='branch name')
        branch.add_argument('-d', action='store_true',
                            help='deletes the branch')

    def execute(self, repository, args):
        branch = args.branch

        if args.d:
            repository.branches.pop(branch)
            print('deleted!')
            return

        if branch in repository.branches:
            print('this branch has already existed!')
            return

        head_commit = repository.branches['head']
        repository.branches[branch] = head_commit
        print('branched!')
