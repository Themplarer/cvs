from pathlib import Path
from random import randint

from commands.command import Command
from utils.file_utils import get_files, read_file


def _get_joke(number):
    jokes_dir_path = Path(f'commands/easter_eggs/jokes')

    if not (number and (jokes_dir_path / f'{number}.txt').exists()):
        number = randint(1, len(get_files('*', jokes_dir_path)))

    return number, read_file(jokes_dir_path / f'{number}.txt')


class Joke(Command):
    def configure(self, subparsers):
        joke = subparsers.add_parser('joke')
        joke.set_defaults(func=self.execute)
        joke.add_argument('-n', '--number', required=False)

    def execute(self, repository, args):
        number, joke = _get_joke(args.number)
        print('Внимание, анекдот', number)
        for i in joke:
            print(i)
