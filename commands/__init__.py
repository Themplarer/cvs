__all__ = ['Add', 'Branch', 'Checkout', 'Commit', 'Diff', 'Init', 'Log',
           'Merge', 'Status', 'Tag', 'Credits', 'Joke', 'Pull', 'Push',
           'Clone', 'Fetch']

from commands.add import Add
from commands.branch import Branch
from commands.checkout import Checkout
from commands.commit import Commit
from commands.diff import Diff
from commands.easter_eggs.credits import Credits
from commands.easter_eggs.joke import Joke
from commands.easter_eggs.remotes import Push, Fetch, Clone, Pull
from commands.init import Init
from commands.log import Log
from commands.merge import Merge
from commands.status import Status
from commands.tag import Tag
