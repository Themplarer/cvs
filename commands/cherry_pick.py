from commands.command import Command


class CherryPick(Command):
    _help_string = 'Cherry-picks commit specified by hash'

    def configure(self, subparsers):
        cherry_pick = subparsers.add_parser('cherry-pick',
                                            help=self._help_string)
        cherry_pick.set_defaults(func=self.execute)
        cherry_pick.add_argument('commit', help='hash of some commit')

    def execute(self, repository, args):
        print('WORK IN PROGRESS')
