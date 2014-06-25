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
        if inspect.isclass(v) and issubclass(v,Plugin) and Plugin != v and v.id == name:
            plugin = v()
            break
    return plugin

def valid_json(json):
    #Check that we have the basic properties in place. 
    #We can't check if the data is correct as this is plugin specific
    if not isinstance(json,dict):
        Logger().error("Command is not a dictionary")
        return False
    if 'name' not in json.keys():
        Logger().error("No 'name' key was found in the command")
        return False
    if 'data' not in json.keys():
        return False
    if json['type'] not in ['sync','async']:
        return False
    return True
    

def commandReceived(self, jsondata):
    '''Called when a command is received. It parses the json and calls the correct plugin passing in the data.'''
    global listener
    try:
        data = json.loads(jsondata)
    except Exception, e:
        Logger().error("Invalid JSON string: " + jsondata)
        #No point in going any further
        callback("",2,{"error":"Invalid JSON string"})
        return
    Logger().info("Parsed: " + str(data))
    if 'type' not in data.keys():
        Logger().warning("No 'type' key was found in the command. Assuming sync")
        data['type'] = 'sync'
    if not valid_json(data):
        Logger().error("Command was not valid")
        callback("",2,{"error":"Invalid JSON string"})
        return
    
    try:
        pluginName = data['name']
        plugin = getPlugin(pluginName)
    except Exception, e:
        Logger().error("Unable to get plugin")
        callback("",3,{"error":"Plugin not found"})
        return
    if plugin != None:
        try:
            plugin.run(callback,data['data'])
        except Exception, e:
            callback("",4,{"error":str(e.__class__) + ": " + str(e)})
            Logger().error("Plugin run failed: " + str(e.__class__) + ': ' + str(e))
    else:
        if pluginName != None and pluginName != "":
            callback(pluginName,3,{"error":"Plugin not found"})
        else:
            callback("",3,{"error":"Plugin not found"})
        Logger().error("Plugin '" + pluginName + "' not found")
        
def connectionFormed(self):
    '''Called when a new connection is formed.'''
    #TODO: I have self because a class passes self back into the method...
    Logger().info("Client connection")


def callback(plugin,code,values):
    '''The callback method provided to the plugin so that the response can be issued.'''
    global listener
    #For the code, it is plugin specific, however it is recommended to use the following:
    #0 - Command successful
    #1 - Unsupported command
    #2 - Invalid command
    #3 - Plugin not found
    #4 - Command unsuccessful
    if values == None:
        values = ""
    if type(plugin) == str:
        listener.sendResponse({"plugin":plugin,"code":code,"values":values})
    else:
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
            Logger().error('Invalid listener. Quitting.')
            sys.exit(1)
    else:
        Logger().warning('No argument specified, defaulting to SocketListener()')
        listener = SocketListener()
    while(True):
        #We want this to start running again should it fail
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
