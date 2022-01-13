from commands.command import RepositoryDependentCommand


class CherryPick(RepositoryDependentCommand):
    _help_string = 'Cherry-picks commit specified by hash'

    def configure(self, subparsers):
        cherry_pick = subparsers.add_parser('cherry-pick',
                                            help=self._help_string)
        cherry_pick.set_defaults(obj=self)
        cherry_pick.add_argument('commit', help='hash of some commit')

    def execute(self, repository, args, writer):
        super().execute(repository, args, writer)

        writer.write('WORK IN PROGRESS')
