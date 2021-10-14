from argsparseerror import ArgsParseError
from commands.command import Command


class Help(Command):
    help_string = '''Usage: python ./main.py help [command]
    command - name of goodgit command, optional argument

    Writes this text if command is not specified.
    Otherwise, writes help of other command
    
    TODO: write short explanation of commands'''

    def parse_args(self, args):
        if len(args) > 1:
            raise ArgsParseError
        return {'command': i for i in args}

    def execute(self, caller, args):
        print('ye i\'ll help u')
        if len(args) == 0:
            print(self.help_string)
        else:
            print(caller.oper_dict[args['command']]().help_string)