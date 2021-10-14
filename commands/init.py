import os
from commands.command import Command
from utils import create_file


class Init(Command):
    help_string = '''Usage: python ./main.py init [path]
    path - directory, optional argument
    
    Creates files and directories for internal purposes.
    Starts at path directory if specified or at current directory'''

    def execute(self, caller, args):
        if caller.is_initiated():
            print('cvs has already been initiated!')
            return

        if not os.path.exists('.gitignore'):
            create_file('.gitignore')

        os.mkdir(caller.dir_path)
        os.chdir(caller.dir_path)
        os.mkdir('./commits')
        create_file('index')

        with open('main', 'w') as f:
            f.write('''KHOROSHiy_git v.1.0\n__________
master|\n__________\nhead:\nmaster:''')
        print('initiated')
