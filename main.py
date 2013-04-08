from PowerManager import PowerManager
from Messager import *
from twisted.internet import protocol, reactor
import json

def getPlugin(name):
	print name
	if name == Messager.id:
		return Messager()
	else:
		return None

class PluginResponse(protocol.Protocol):
    def dataReceived(self, data):
		d = json.loads(data)
		print d
		pluginName = d.keys()[0]
		p = getPlugin(pluginName)
		p.run(callback,d[pluginName])
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

	
