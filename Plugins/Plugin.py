class Plugin(object):
    """A base class for Plugin objects"""

    def run(self, callback, arguments):
        raise NotImplementedError("Not Implemented")
