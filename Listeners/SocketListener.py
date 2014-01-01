from Listener import Listener
from twisted.internet import protocol, reactor
from Utilities import *

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
    '''An implementation of the listener class which listens for data on a single socket.'''
    
    def __init__(self):
        Listener.__init__(self)
        
    def sendResponse(self, response):
        Logger().info("SENDING RESPONSE: " + str(response))
        
    def run(self, connectionFormed, commandReceived):
        PluginResponse.commandReceived = commandReceived
        PluginResponse.connectionFormed = connectionFormed
        reactor.listenTCP(22001, PluginListenerFactory())
        reactor.run()
        
    def quit(self):
        reactor.stop()
        

