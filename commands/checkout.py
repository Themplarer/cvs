from commands.command import Command


class Checkout(Command):
    _help_string = 'Switches to that branch'
    _commit_warning = 'be careful: it\'s impossible to commit at this pointer!'

    def configure(self, subparsers):
        checkout = subparsers.add_parser('checkout', help=self._help_string)
        checkout.set_defaults(func=self.execute)
        checkout.add_argument('pointer', help='name for new checkout')

    def execute(self, repository, args):
        if args.pointer in repository.branches:
            repository.selected_branch = args.pointer
            print('checked out branch', args.pointer)
            return

        if args.pointer in repository.tags:
            repository.selected_branch = args.pointer
            print('checked out tag', args.pointer)
            print(self._commit_warning)
            return

        if args.pointer in repository.commits:
            repository.selected_branch = args.pointer
            print('checked out commit', args.pointer)
            print(self._commit_warning)
            return

        print(
            'there is no suitable pointer (commit, tag, branch) to checkout!')
