from commands.command import Command


class Branch(Command):
    _help_string = 'Creates new branch based on head'

    def configure(self, subparsers):
        branch = subparsers.add_parser('branch', help=self._help_string)
        branch.set_defaults(func=self.execute)
        branch.add_argument('branch', help='name for new branch')

    def execute(self, caller, args):
        head_commit = caller.branches["head"]

        with open('./.goodgit/main', 'a') as f:
            f.write(
                f'\n{args.branch}:{"" if not head_commit else head_commit}')

        print('branched')
