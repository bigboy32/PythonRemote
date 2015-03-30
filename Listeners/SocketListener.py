from twisted.internet import protocol, reactor
from Listener import Listener
from Utilities import *
import json

class PluginResponse(protocol.Protocol):

    commandReceived = None
    connectionFormed = None

    def __init__(self):
        pass

    def dataReceived(self, data):
        self.commandReceived(data)

    def connectionMade(self):
        self.connectionFormed()


class PluginListenerFactory(protocol.Factory):
    def __init__(self):
        self.responders = []

    def buildProtocol(self, address):
        response = PluginResponse()
        self.responders.append(response)
        return response


class SocketListener(Listener):
    """An implementation of the listener class which listens for data on a single socket."""

    def __init__(self, port=22000):
        Listener.__init__(self)
        self.port = port

    def send_response(self, response):
        Logger().info("SENDING RESPONSE: " + str(response))
        self.plugin_listener_factory.responders[0].transport.write(json.dumps(response))

    def run(self, connection_formed, command_received):
        PluginResponse.commandReceived = command_received
        PluginResponse.connectionFormed = connection_formed
        self.plugin_listener_factory = PluginListenerFactory()
        # noinspection PyUnresolvedReferences
        reactor.listenTCP(self.port, self.plugin_listener_factory)
        # noinspection PyUnresolvedReferences
        reactor.run()

    def quit(self):
        # noinspection PyUnresolvedReferences
        reactor.stop()
        

