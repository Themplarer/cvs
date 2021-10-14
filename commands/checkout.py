import re

from argsparseerror import ArgsParseError
from commands.command import Command


class Checkout(Command):
    help_string = '''Usage: python ./main.py checkout [branchName]
    branchName - name of branch to checkout, compulsory argument
    
    Switches to that branch'''

    def parse_args(self, args):
        if len(args) != 1:
            raise ArgsParseError
        return {'branchName': i for i in args}

    def execute(self, caller, args):
        with open('./.goodgit/main') as f:
            content = f.read()

        content = re.sub(r'(.*?)|', f'{args["branchName"]}|', content)

        with open('./.goodgit/main', 'w') as f:
            f.write(content)
