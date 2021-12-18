from pathlib import Path

from commands.command import Command


class Init(Command):
    _help_string = 'Creates files and directories for internal purposes. ' \
                   'Starts at `path` directory if specified or at current ' \
                   'directory'

    def configure(self, subparsers):
        init = subparsers.add_parser('init', help=self._help_string)
        init.set_defaults(func=self.execute)
        init.add_argument('-p', '--path', help='directory path')

    def execute(self, repository, args):
        if repository.is_initiated:
            print('goodgit has already been initiated!')
            return

        Path('.gitignore').touch(exist_ok=True)
        path = Path(args.path if args.path else '.') / repository.dir_path
        path.mkdir(exist_ok=True)
        (path / 'commits').mkdir()
        (path / 'stashes').mkdir()
        (path / 'index').touch()

        repository.branches['master'] = None
        repository.branches['head'] = None
        print('initiated')
