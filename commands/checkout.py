from commands.command import RepositoryDependentCommand


class Checkout(RepositoryDependentCommand):
    _help_string = 'Switches to that branch'
    _commit_warning = 'be careful: it\'s impossible to commit at this pointer!'
    _not_found = 'there is no suitable pointer (commit, tag or branch) ' \
                 'to checkout!'

    def configure(self, subparsers):
        checkout = subparsers.add_parser('checkout', help=self._help_string)
        checkout.set_defaults(obj=self)
        checkout.add_argument('pointer', help='name for new checkout')

    def execute(self, repository, args, writer):
        super().execute(repository, args, writer)

        if args.pointer in repository.branches:
            repository.selected_branch = args.pointer
            writer.write('checked out branch', args.pointer)
            return

        if args.pointer in repository.tags:
            repository.selected_branch = args.pointer
            writer.write('checked out tag', args.pointer)
            writer.write(self._commit_warning)
            return

        if args.pointer in repository.commits:
            repository.selected_branch = args.pointer
            writer.write('checked out commit', args.pointer)
            writer.write(self._commit_warning)
            return

        writer.write(self._not_found)
