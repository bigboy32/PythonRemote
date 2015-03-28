from Plugins import *
from Listeners import *
from Utilities import *
import json
import sys
import inspect

class PycmoteServer(Plugin): #We are also a plugin as we can then respond and act on server events

    id = "server"

    def __init__(self):
        Plugin.__init__(self)
        self.listener = None
        self.plugins = {}

    def set_listener(self, listener):
        self.listener = listener

    def run_listener(self):
        self.listener.run(self.connectionFormed, self.commandReceived)

    def run(self, callback, args):
        if "command" not in args.keys():
            callback(self, 1, {"error":"No command specified"})

        if args["command"] == "quit":
            callback(self, 0, None)
            self.listener.quit()
        else:
            callback(self, 2, {"error":"Command not supported"})

    def getPlugin(self, name):
        '''Returns an instance of the plugin specified by the name passed in'''

        Logger().info("Plugin requested: " + name)

        #Load all plugins if we need to
        if self.plugins == {}:
            for k,v in globals().iteritems():
                #Get all subclasses of Plugin (but exclude Plugin itself and the server (which is always available)
                if inspect.isclass(v) and issubclass(v,Plugin) and Plugin != v and v.id != "server":
                    self.plugins[v.id] = {}
                    self.plugins[v.id]["activated"] = False
                    self.plugins[v.id]["plugin"] = v

                #Add the server
                self.plugins[self.id] = {"activated":True, "plugin":self}

        try:
            requested_plugin = self.plugins[name]
            if not requested_plugin["activated"]:
                requested_plugin["plugin"] = requested_plugin["plugin"]()
                requested_plugin["activated"] = True

            return requested_plugin["plugin"]
        except KeyError, e:
            Logger().info("Plugin '" + name + "' not found.")
            return None


    def valid_json(self, json):
        #Check that we have the basic properties in place.
        #We can't check if the data is correct as this is plugin specific
        if not isinstance(json,dict):
            Logger().error("Command is not a dictionary")
            return False
        if 'name' not in json.keys():
            Logger().error("No 'name' key was found in the command")
            return False
        if 'data' not in json.keys():
            json["data"] = {}
        if json['type'] not in ['sync','async']:
            return False
        return True

    def commandReceived(self, jsondata):
        '''Called when a command is received. It parses the json and calls the correct plugin passing in the data.'''
        try:
            data = json.loads(jsondata)
        except Exception, e:
            Logger().error("Invalid JSON string: " + jsondata)
            #No point in going any further
            self.callback("", 2, {"error":"Invalid JSON string"})
            return
        Logger().info("Parsed: " + str(data))
        if 'type' not in data.keys():
            Logger().warning("No 'type' key was found in the command. Assuming sync")
            data['type'] = 'sync'
        if not self.valid_json(data):
            Logger().error("Command was not valid")
            self.callback("",2,{"error":"Invalid JSON string"})
            return

        try:
            pluginName = data['name']
            plugin = self.getPlugin(pluginName)
        except Exception, e:
            Logger().error("Unable to get plugin")
            self.callback("",3,{"error":"Plugin not found"})
            return
        if plugin != None:
            try:
                plugin.run(self.callback,data['data'])
            except Exception, e:
                self.callback("",4,{"error":str(e.__class__) + ": " + str(e)})
                Logger().error("Plugin run failed: " + str(e.__class__) + ': ' + str(e))
        else:
            if pluginName != None and pluginName != "":
                self.callback(pluginName,3,{"error":"Plugin not found"})
            else:
                self.callback("",3,{"error":"Plugin not found"})
            Logger().error("Plugin '" + pluginName + "' not found")

    def connectionFormed(self):
        '''Called when a new connection is formed.'''
        #TODO: I have self because a class passes self back into the method...
        Logger().info("Client connection")


    def callback(self, plugin, code, values):
        '''The callback method provided to the plugin so that the response can be issued.'''
        #For the code, it is plugin specific, however it is recommended to use the following:
        #0 - Command successful
        #1 - Unsupported command
        #2 - Invalid command
        #3 - Plugin not found
        #4 - Command unsuccessful
        if values == None:
            values = ""
        if type(plugin) == str:
            self.listener.sendResponse({"plugin":plugin,"code":code,"values":values})
        else:
            self.listener.sendResponse({"plugin":plugin.id,"code":code,"values":values})


def main():
    '''Main method which loads a listener and starts it'''
    server = PycmoteServer()

    if(len(sys.argv) > 1):
        if(sys.argv[1] == 'socket'):
            Logger().info('Creating SocketListener()')
            server.set_listener(SocketListener())
        elif(sys.argv[1] == 'ssh'):
            Logger().info('Creating SSHListener()')
            server.set_listener(SSHListener())
        else:
            Logger().error('Invalid listener. Quitting.')
            sys.exit(1)
    else:
        Logger().warning('No argument specified, defaulting to SocketListener()')
        server.set_listener(SocketListener())
    while(True):
        #We want this to start running again should it fail
        try:
            Logger().info("Running listener")
            server.run_listener()
            Logger().info("Listener completed its task. Running again.")
        except Exception,e:
            Logger().error('Listener failed: ' + str(e))
            traceback.print_exc()
    
if __name__ == '__main__':
     main() 
