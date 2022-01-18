from pathlib import Path

from commands.command import Command


class Init(Command):
    _help_string = 'Creates files and directories for internal purposes'

    def configure(self, subparsers):
        init = subparsers.add_parser('init', help=self._help_string)
        init.set_defaults(obj=self)

    def execute(self, repository, args, writer):
        if repository.is_initiated:
            writer.write('goodgit has already been initiated!')
            return

        with Path('.gitignore').open(mode='a') as f:
            f.write('.goodgit\n')

        if repository.dir_path.exists():
            writer.write('goodgit directory has already existed '
                         'but it is not initiated! '
                         'consider checking it out and deleting')
            return

        for i in [repository.dir_path, repository.dir_path / 'commits',
                  repository.dir_path / 'stashes']:
            i.mkdir()

        (repository.dir_path / 'index').touch()
        repository.branches['master'] = None
        repository.branches['head'] = None
        writer.write('initiated')
