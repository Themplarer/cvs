from commands.command import Command


class RemoteCommand(Command):
    def __init__(self, command_name):
        self._name = command_name
        self._text = 'not available in free version!'

    def configure(self, subparsers):
        subparsers.add_parser(self._name).set_defaults(func=self.execute)

    def execute(self, repository, args):
        print(self._text)


class Push(RemoteCommand):
    def __init__(self):
        super().__init__('push')


class Fetch(RemoteCommand):
    def __init__(self):
        super().__init__('fetch')


class Pull(RemoteCommand):
    def __init__(self):
        super().__init__('pull')


class Clone(RemoteCommand):
    def __init__(self):
        super().__init__('clone')
