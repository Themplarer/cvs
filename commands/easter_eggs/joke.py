import random
from os import chdir

from commands.command import Command
from utils import exists, get_files, read_file


class Joke(Command):
    jokes_dir_path = './commands/easter_eggs/jokes/'

    def configure(self, subparsers):
        joke = subparsers.add_parser('joke')
        joke.set_defaults(func=self.execute)
        joke.add_argument('-n', '--number', required=False)

    def execute(self, caller, args):
        number, joke = self._get_joke(args.number)
        print('Внимание, анекдот', number)
        for i in joke:
            print(i)

    def _get_joke(self, number):
        chdir(self.jokes_dir_path)
        if not (number and exists(f'{number}.txt')):
            number = random.randint(1, len(get_files('**')))

        return number, read_file(f'{number}.txt')

