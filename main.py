from Plugins import *
from Listeners import *
from Utilities import *
import json
import sys
import inspect

def getPlugin(name):
    '''Returns an instance of the plugin specified by the name passed in'''
    
    global listener
    if name == 'quit':
        listener.quit()
        return None
    
    plugin = None
    
    Logger().info("Plugin name:" + name)
    for k,v in globals().iteritems():
        if inspect.isclass(v):
            if issubclass(v,Plugin) and Plugin != v:
                if v.id == name:
                    plugin = v()
                    break
    return plugin

def commandReceived(self, jsondata):
    '''Called when a command is received. It parses the json and calls the correct plugin passing in the data.'''
    global listener
    Logger().info("JSON RECEIVED: " + str(jsondata))
    data = json.loads(jsondata)
    Logger().info("PARSED DATA: " + str(data))
    pluginName = data['name']
    plugin = getPlugin(pluginName)
    if plugin != None:
        plugin.run(callback,data['data'])
        
def connectionFormed(self):
    '''Called when a new connection is formed.'''
    #TODO: I have self because a class passes self back into the method...
    Logger().info("Client connection")


def callback(plugin,code,values):
    '''The callback method provided to the plugin so that the response can be issued.'''
    global listener
    listener.sendResponse({"plugin":plugin.id,"code":code,"values":values})

listener = None
    
def main():
    '''Main method which loads a listener and starts it'''
    global listener
    if(len(sys.argv) > 1):
        if(sys.argv[1] == 'socket'):
            Logger().info('Creating SocketListener()')
            listener = SocketListener()
        elif(sys.argv[1] == 'ssh'):
            Logger().info('Creating SSHListener()')
            listener = SSHListener()
        else:
            Logger().error('No listener specified')
            sys.exit(0)
    else:
        Logger().warning('No arguement specified, defaulting to SocketListener()')
        listener = SocketListener()
    while(True):
        #We want this to start running again
        try:
            Logger().info("Running listener")
            listener.run(connectionFormed,commandReceived)
            Logger().info("Listener completed its task. Running again.")
        except Exception,e:
            Logger().error('Listener failed: ' + str(e))
            traceback.print_exc()
    #And so the main code ends....
    
if __name__ == '__main__':
     main() 

    
