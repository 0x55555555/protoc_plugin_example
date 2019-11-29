
def parse_path(self, struct, path):
    """Return the correct thing for a full path.
    Args:
        struct (:class:`google.protobuf.Message`): The structure being
            parsed.
        path (list): The path; a list of numbers. See descriptor.proto
            for complete documentation.
    Returns:
        :class:`protoc_docs.code.MessageStructure`: A ``MessageStructure``
            object. The same object may be returned over multiple
            iterations (for example, if the loop calling this function
            does so for a class and its members); however, these return
            objects are hashable and therefore may safely be added
            to a set to handle de-duplication.
    """
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