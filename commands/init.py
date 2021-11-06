import os
from commands.command import Command
from utils import create_file, exists, write_file


class Init(Command):
    _help_string = 'Creates files and directories for internal purposes. ' \
                   'Starts at path directory if specified or at current ' \
                   'directory'

    def configure(self, subparsers):
        init = subparsers.add_parser('init', help=self._help_string)
        init.set_defaults(func=self.execute)
        init.add_argument('-p', '--path', help='directory path')

    def execute(self, caller, args):
        if caller.is_initiated():
            print('cvs has already been initiated!')
            return

        if not exists('.gitignore'):
            create_file('.gitignore')

        path = args.path
        if path:
            os.chdir(path)

        os.mkdir(caller.dir_path)
        os.chdir(caller.dir_path)
        os.mkdir('./commits')
        create_file('index')
        write_file('main', ['KHOROSHiy_git v.1.0',
                            '__________',
                            'master|',
                            '__________',
                            'head:',
                            'master:'])
        print('initiated')
