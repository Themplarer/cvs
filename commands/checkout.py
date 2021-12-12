import re

from commands.command import Command


class Checkout(Command):
    _help_string = 'Switches to that branch'

    def configure(self, subparsers):
        checkout = subparsers.add_parser('checkout', help=self._help_string)
        checkout.set_defaults(func=self.execute)
        checkout.add_argument('branch', help='name for new checkout')

    def execute(self, repository, args):
        if args.branch not in repository.branches:
            print('there is no such branch!')
            return

        with repository.main_file_path.open() as f:
            content = f.read()

        content = re.sub(r'(.*?)|', f'{args.branch}|', content)
        content = re.sub(r'head:.*^',
                         f'head:{repository.branches[args.branch].hash}',
                         content)
        with repository.main_file_path.open('w') as f:
            f.write(content)
