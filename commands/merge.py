from commands.command import Command


class Merge(Command):
    _help_string = 'Merges specified branch into head'

    def configure(self, subparsers):
        merge = subparsers.add_parser('merge', help=self._help_string)
        merge.set_defaults(func=self.execute)
        merge.add_argument('branch', help='name of branch')

    def execute(self, repository, args):
        print('WORK IN PROGRESS!')
