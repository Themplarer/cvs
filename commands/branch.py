from argsparseerror import ArgsParseError
from commands.command import Command


class Branch(Command):
    help_string = '''Usage: python ./main.py branch [branchName]
    branchName - name for new branch, compulsory argument
    
    Creates new branch based on head'''

    def parse_args(self, args):
        if len(args) != 1:
            raise ArgsParseError
        return {'branchName': i for i in args}

    def execute(self, caller, args):
        head_commit = caller.branches["head"]

        with open('./.goodgit/main', 'a') as f:
            f.write(f'\n{args["branchName"]}:'
                    f'{"" if not head_commit else head_commit}')

        print('branched')
