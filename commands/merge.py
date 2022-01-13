from commands.command import RepositoryDependentCommand


class Merge(RepositoryDependentCommand):
    _help_string = 'Merges specified branch into head'

    def configure(self, subparsers):
        merge = subparsers.add_parser('merge', help=self._help_string)
        merge.set_defaults(obj=self)
        merge.add_argument('branch', help='name of branch')

    def execute(self, repository, args, writer):
        super().execute(repository, args, writer)

        writer.write('WORK IN PROGRESS!')
