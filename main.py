from PowerManager import PowerManager
from Messager import *
from twisted.internet import protocol, reactor

class PluginResponse(protocol.Protocol):
    def dataReceived(self, data):
		print data
        #self.transport.write(data)

class PluginListenerFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return PluginResponse()

def callback(plugin,code,values):
	print plugin
	print code
	print values

def main():
	reactor.listenTCP(22001, PluginListenerFactory())
	reactor.run()
	#p = Messager()
	#print p.getOS()
	#p.run(callback,{'type':'okcancel','title':'Message Title','message':'Hello World'})




if __name__ == '__main__':
 	main() 

	
