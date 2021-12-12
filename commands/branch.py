from commands.command import Command


class Branch(Command):
    _help_string = 'Creates new branch based on head'

    def configure(self, subparsers):
        branch = subparsers.add_parser('branch', help=self._help_string)
        branch.set_defaults(func=self.execute)
        branch.add_argument('branch', help='name for new branch')

    def execute(self, repository, args):
        branch = args.branch
        if repository.selected_branch == branch:
            print('this branch has already existed!')
            return

        head_commit = repository.branches['head']
        head = head_commit if head_commit else ''

        with repository.main_file_path.open('a') as f:
            f.write(f'\n{branch}:{head}')

        print('branched')
