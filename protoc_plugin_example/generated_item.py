
class GeneratedItem:
    def __init__(self, id, content):
        self._id = id
        self._filename = "%s.rst" % id
        self._content = content

    @property
    def id(self):
        return self._id

    @property
    def filename(self):
        return self._filename

    @property
    def content(self):
        return self._content