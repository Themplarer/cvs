from utils.file_utils import read_file, get_files, write_file
from commands.command import Command


class Add(Command):
    _help_string = 'Adds specified files and directories to the index'

    def configure(self, subparsers):
        add = subparsers.add_parser('add', help=self._help_string)
        add.set_defaults(func=self.execute)
        add.add_argument('path',
                         help='kind of filter for directories and files')

    def execute(self, caller, args):
        files = get_files(args.path, read_file(caller.dir_path + '/index'),
                          True)
        write_file(caller.dir_path + '/index', files)
        print('added')
