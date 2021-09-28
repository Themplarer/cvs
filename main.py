import os
import re
from sys import argv
import pathlib


# todo refactor all
# todo переделать проверку файлов на включение в список

def init(args):
    if len(args) > 0:
        print('invalid usage')

    if os.path.exists(dir_path) and os.path.exists(dir_path + 'main'):
        print('cvs has already been initiated!')
        return

    if not os.path.exists('.gitignore'):
        open('.gitignore', 'w').close()

    os.mkdir(dir_path)
    os.chdir(dir_path)
    os.mkdir('./master/')
    open('index', 'w').close()

    with open('main', 'w') as f:
        f.write('KHOROSHiy_git v.1.0\n__________\nmaster:')
    print('initiated')


def ignorre(ignore_set, x):
    res = [re.compile(i.replace('\\', '/')) for i in ignore_set]
    return list(filter(lambda s: f(s, res), map(lambda i: str(i).replace('\\', '/'), x)))


def f(s, res):
    for i in res:
        if i.match(s):
            return False

    return True


def help(args):
    print('ye i\'ll help u')


def add(args):
    if len(args) != 1:
        print('incorrect usage')
        return

    _comments = re.compile(r'^(#.*)| $')
    with open('.gitignore') as f:
        ignore = {i.replace('\\', '/').replace('*', '.*') + '.*' for i in (filter(lambda x: not len(x) == 0 and not _comments.match(x), f.read().splitlines()))}

    _path = pathlib.Path(args[0])
    files = {str(i) for i in ignorre(ignore, [_path] if _path.is_file() else list(_path.rglob('*')))}

    with open(dir_path + 'index') as f:
        files = files.union(set(f.read().splitlines()))

    with open(dir_path + 'index', 'w') as f:
        f.writelines('\n'.join(files))

    print('added')


def execute(args):
    oper_dict[args[0]](args[1:])


dir_path = './.goodgit/'
oper_dict = {'init': init, 'help': help, 'add': add}

if __name__ == '__main__':
    if len(argv) < 2:
        # todo add 'help'
        print('type \'help\' lol')
    else:
        oper_dict[argv[1]](argv[2:])
