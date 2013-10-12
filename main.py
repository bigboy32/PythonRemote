from PowerManager import PowerManager
from SocketListener import *
from Messager import *
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

def commandReceived(self, data):
    print data
    d = json.loads(data)
    print d
    pluginName = d['name']
    p = getPlugin(pluginName)
    p.run(callback,d['data'])
    #self.transport.write(data)
        
def connectionFormed(self):
    #TODO: I have self because a class passes self back into the method...
    print "Client connection"


def callback(plugin,code,values):
    print plugin
    print code
    print values

def main():
    listener = None
    if(len(sys.argv) > 1):
        print 'has arg'
        if(sys.argv[1] == 'socket'):
            print 'arg is socket'
            listener = SocketListener()
        else:
            print 'No listener specified'
            sys.exit(0)
    else:
        print 'no arg'
        listener = SocketListener()
    listener.run(connectionFormed,commandReceived)




if __name__ == '__main__':
     main() 

    
