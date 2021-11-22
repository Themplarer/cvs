import re

from utils import read_file, get_files, write_file
from commands.command import Command


class Status(Command):
    _help_string = 'Writes kind of changes for different files'

    def configure(self, subparsers):
        status = subparsers.add_parser('status', help=self._help_string)
        status.set_defaults(func=self.execute)

    def execute(self, caller, args):
        indexed_files = get_files('**')
        last_commit = set(caller.branches["head"])
        changes = dict()

        # for i in indexed_files:
        #     if

        print('added')
