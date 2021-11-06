class Command:
    def configure(self, subparsers):
        pass

    def execute(self, caller, args):
        print(len(args))
