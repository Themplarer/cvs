from commands.command import Command


class Tag(Command):
    _help_string = 'Does something to some tag. ' \
                   'Default - creates a new based on head'

    def configure(self, subparsers):
        tag = subparsers.add_parser('tag', help=self._help_string)
        tag.set_defaults(func=self.execute)
        tag.add_argument('tag', help='tag name')
        tag.add_argument('-d', action='store_true', help='deletes the tag')

    def execute(self, repository, args):
        tag = args.tag

        if args.d:
            repository.tags.pop(tag)
            print('deleted!')
            return

        if tag in repository.tags:
            print('this tag has already existed!')
            return

        head_commit = repository.branches['head']
        repository.tags[tag] = head_commit
        print('taged!')
