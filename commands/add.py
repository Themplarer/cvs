from pathlib import Path

from utils.file_utils import read_file, get_files, write_file
from commands.command import Command


class Add(Command):
    _help_string = 'Adds specified files and directories to the index'

    def configure(self, subparsers):
        add = subparsers.add_parser('add', help=self._help_string)
        add.set_defaults(func=self.execute)
        add.add_argument('path',
                         help='kind of filter for directories and files')

    def execute(self, repository, args):
        index_path = repository.dir_path / 'index'
        initial_files = [Path(i) for i in read_file(index_path)]
        files = (i.as_posix() for i in
                 get_files(args.path, '.', initial_files, True))
        write_file(index_path, files)
        print('added')
