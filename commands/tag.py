from commands.command import Command


class Tag(Command):
    _help_string = 'Does something to some tag. ' \
                   'Default - shows list of all tags'

    def configure(self, subparsers):
        tag = subparsers.add_parser('tag', help=self._help_string)
        tag.set_defaults(func=self.execute)
        tag.add_argument('tag', help='tag name', nargs='?')
        tag.add_argument('-d', action='store_true', help='deletes the tag')

    def execute(self, repository, args):
        if not args.tag:
            for i in repository.tags.keys():
                print(i)

            return

        tag = args.tag
        if args.d:
            if tag in repository.tags:
                repository.tags.pop(tag)
                print('deleted!')
            else:
                print('there is no such tag!')

            return

        if tag in repository.tags:
            print('this tag has already existed!')
            return

        head_commit = repository.branches['head']
        repository.tags[tag] = head_commit
        print('taged!')
