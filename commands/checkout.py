import re

from commands.command import Command


class Checkout(Command):
    _help_string = 'Switches to that branch'

    def configure(self, subparsers):
        checkout = subparsers.add_parser('checkout', help=self._help_string)
        checkout.set_defaults(func=self.execute)
        checkout.add_argument('branch', help='name for new checkout')

    def execute(self, caller, args):
        with open('./.goodgit/main') as f:
            content = f.read()

        content = re.sub(r'(.*?)|', f'{args.branch}|', content)
        with open('./.goodgit/main', 'w') as f:
            f.write(content)
