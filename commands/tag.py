from commands.command import RepositoryDependentCommand


class Tag(RepositoryDependentCommand):
    _help_string = 'Does something to some tag. ' \
                   'Default - shows list of all tags'

    def configure(self, subparsers):
        tag = subparsers.add_parser('tag', help=self._help_string)
        tag.set_defaults(obj=self)
        tag.add_argument('tag', help='tag name', nargs='?')
        tag.add_argument('-d', action='store_true', help='deletes the tag')

    def execute(self, repository, args, writer):
        super().execute(repository, args, writer)

        if not args.tag:
            if args.d:
                writer.write('called to delete a tag but tag is not '
                             'specified')
                return

            for i in repository.tags.keys():
                writer.write(i)
            return

        tag = args.tag
        if args.d:
            if tag in repository.tags:
                repository.tags.pop(tag)
                writer.write('deleted!')
            else:
                writer.write('there is no such tag!')

            return

        if tag in repository.tags:
            writer.write('this tag has already existed!')
            return

        repository.tags[tag] = repository.branches['head']
        writer.write('taged!')
