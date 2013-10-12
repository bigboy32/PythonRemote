from Listener import Listener
from twisted.internet import protocol, reactor

class PluginResponse(protocol.Protocol):
    
    commandReceived = None
    connectionFormed = None
    
    def dataReceived(self, data):
        self.commandReceived(data)
    
    def connectionMade(self):
        self.connectionFormed()

class PluginListenerFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return PluginResponse()


class SocketListener(Listener):

    def __init__(self):
        Listener.__init__(self)
        
    def run(self, connectionFormed, commandReceived):
        PluginResponse.commandReceived = commandReceived
        PluginResponse.connectionFormed = connectionFormed
        reactor.listenTCP(22001, PluginListenerFactory())
        reactor.run()
        

