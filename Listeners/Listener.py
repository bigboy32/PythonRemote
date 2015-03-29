class Listener(object):
    """A base class for all listener objects"""

    def run(self, connection_formed, command_received):
        """The code to run while listening for connections and instructions. """
        raise NotImplementedError("Not Implemented")

    def send_response(self, response):
        raise NotImplementedError("Not Implemented")

    def quit(self):
        raise NotImplementedError("Not Implemented")
