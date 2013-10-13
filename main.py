from Plugins import *
from Listeners import *
import json
import sys

def getPlugin(name):
    '''Returns an instance of the plugin specified by the name passed in'''
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
    '''Called when a command is received. It parses the json and calls the correct plugin passing in the data.'''
    global listener
    print data
    d = json.loads(data)
    print d
    pluginName = d['name']
    if(pluginName == "system"):
        if d['data']['message'] == "quit":
            listener.quit()
    else:
        p = getPlugin(pluginName)
        p.run(callback,d['data'])
        
def connectionFormed(self):
    '''Called when a new connection is formed.'''
    #TODO: I have self because a class passes self back into the method...
    print "Client connection"


def callback(plugin,code,values):
    '''The callback method provided to the plugin so that the response can be issued.'''
    global listener
    listener.sendResponse({"plugin":plugin.id,"code":code,"values":values})

listener = None
    
def main():
    '''Main method which loads a listener and starts it'''
    global listener
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
    print "Quitting"




if __name__ == '__main__':
     main() 

    
