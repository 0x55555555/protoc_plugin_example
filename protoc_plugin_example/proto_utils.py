import collections
import logging
import textwrap

class CommentStructure(object):
    """A class representing the structure for a proto message.
    This class is its own registry; calling the with the same message name
    will return the same object.
    """
    _registry = {}

    @classmethod
    def get(cls, name):
        return cls._registry[name]

    @classmethod
    def get_or_create(cls, name):
        """Return a Message object.
        Args:
            name (str): The fully qualified name of the message (for example:
                ``google.protobuf.SourceCodeInfo``)
        Returns:
            ``MessageStructure``: A ``MessageStructure`` object.
        """
        cls._registry.setdefault(name, cls(name=name))
        return cls._registry[name]

    def __init__(self, name):
        self.name = name
        self.docstring = ''
        self.members = collections.OrderedDict()

    def __hash__(self):
        """Return a hash for this object based on its name.
        This makes MessageStructure objects able to be placed into a set
        to handle de-duplication properly.
        """
        return hash(self.name)

    def __repr__(self):
        tw8 = textwrap.TextWrapper(
            initial_indent=' ' * 8,
            subsequent_indent=' ' * 8,
        )
        tw12 = textwrap.TextWrapper(
            initial_indent=' ' * 12,
            subsequent_indent=' ' * 12,
        )

        answer =  'MessageStructure {\n'
        answer += '    name: {0}\n'.format(self.name)
        answer += '    docstring:\n{0}\n'.format(
            '\n'.join(tw8.wrap(self.docstring)),
        )
        if len(self.members):
            answer += '    members:\n'
        for k, v in self.members.items():
            answer += '        {name}:\n{doc}\n'.format(
                name=k,
                doc='\n'.join(tw12.wrap(v)),
            )
        answer += '}\n'
        return answer

    @classmethod
    def reset(cls):
        cls._registry = {}


def parse_path(struct, path, docstring, message_structure=None):
    """Return the correct thing for a full path.
    Args:
        struct (:class:`google.protobuf.Message`): The structure being
            parsed.
        path (list): The path; a list of numbers. See descriptor.proto
            for complete documentation.
    Returns:
        :class:`CommentStructure`: A ``CommentStructure``
            object. The same object may be returned over multiple
            iterations (for example, if the loop calling this function
            does so for a class and its members); however, these return
            objects are hashable and therefore may safely be added
            to a set to handle de-duplication.
    """

    if len(path) == 0:
        return struct

    # The first two ints in the path represent what kind of thing
    # the comment is attached to (message, enum, or service) and the
    # order of declaration in the file.
    #
    # e.g. [4, 0, ...] would refer to the *first* message, [4, 1, ...] to
    # the second, etc.
    field_name = ''
    for field in [i[0] for i in struct.ListFields()]:
        if field.number == path[0]:
            field_name = field.name
    child = getattr(struct, field_name)[path[1]]
    path = path[2:]

    # If applicable, create the CommentStructure object for this.
    if not message_structure:
        message_structure = CommentStructure.get_or_create(
            name='{pkg}.{name}'.format(
                name=child.name,
                pkg=struct.package,
            ),
        )

    # If the length of the path is 2 or greater, call this method
    # recursively.
    if len(path) >= 2:
        # Nested types are possible.
        #
        # In this case, we need to ensure that we do not lose
        # the outer layers of the nested type name; otherwise the
        # insertion point name will be wrong.
        if not message_structure.name.endswith(child.name):
            message_structure = CommentStructure.get_or_create(
                name='{parent}.{child}'.format(
                    child=child.name,
                    parent=message_structure.name,
                ),
            )
        return parse_path(child, path, docstring, message_structure)

    # Write the documentation to the appropriate spot.
    # This entails figuring out what the Message (basically the "class")
    # is, and then whether this is class-level or property-level
    # documentation.
    if message_structure.name.endswith(child.name):
        message_structure.docstring = docstring
    else:
        message_structure.members[child.name] = docstring

    # If the length of the path is now 1...
    #
    # This seems to be a corner case situation. I am not sure what
    # to do for these, and the documentation for odd-numbered paths
    # does not match my observations.
    #
    # Punting. Most of the docs are better than none of them, which was
    # the status quo ante before I wrote this.
    if len(path) == 1:
        return message_structure

    # Done! Return the message structure.
    return message_structure