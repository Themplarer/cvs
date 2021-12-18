import getpass
import pathlib

from utils.main_file_utils import write_main_file, read_main_file


class Repository:
    author = getpass.getuser()
    dir_path = pathlib.Path('.goodgit')
    main_file_path = dir_path / 'main'
    selected_branch = 'master'
    branches = dict()
    tags = dict()

    def __init__(self):
        if self.is_initiated:
            self.selected_branch, self.branches, self.tags = read_main_file()

    @property
    def is_initiated(self):
        return self.dir_path.exists() and self.main_file_path.exists()

    def save_main_file(self):
        write_main_file(self.selected_branch, self.branches, self.tags)
