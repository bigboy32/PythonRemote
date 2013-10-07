from PowerManager import PowerManager
from Messager import *
from twisted.internet import protocol, reactor
import json
import sys

def getPlugin(name):
	print name
	#TODO: Load this in dynamically
	if name == 'quit':
		sys.exit(0)
	elif name == Messager.id:
		return Messager()
	elif name == PowerManager.id:
	    return PowerManager()
	else:
		return None

class PluginResponse(protocol.Protocol):
	def dataReceived(self, data):
		print data
		d = json.loads(data)
		print d
		pluginName = d['name']
		p = getPlugin(pluginName)
		p.run(callback,d['data'])
		#self.transport.write(data)
	
	def connectionMade(self):
		print "Client connection"

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




if __name__ == '__main__':
 	main() 

	
