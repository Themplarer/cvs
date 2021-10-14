from argsparseerror import ArgsParseError


class Command:
    help_string = 'Default help string'

    def parse_args(self, args):
        if len(args):
            raise ArgsParseError
        return dict()

    def execute(self, caller, args):
        print(len(args))
