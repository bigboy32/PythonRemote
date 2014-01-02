from Plugin import *
import SystemInfo

class PowerManager(Plugin):
    '''The first example class for the python powered remote interface for my computer'''

    id = "power_manager"
    
    def __init__(self):
        Plugin.__init__(self)

    def run(self,callback,args):
        #args is a dictionary of commands and data
        
        if args['option'] == 'sleep':
            if SystemInfo.is_mac():
                callback(self,0,{"answer":"Message received. Sleeping..."})
                os.system("osascript -e 'tell application \"System Events\" to sleep'")
            else:
                callback(self,1,{"answer":"Message received. Unsupported OS"})
                Logger().error("Unsupported OS for command 'sleep'")
        elif args['option'] == 'shutdown':
            callback(self,1,{"answer":"Message received. Unsupported command"})
            Logger().error("Shutdown not yet implemented")
            raise NotImplementedError("Not Implemented")
        elif args['option'] == 'restart':
            callback(self,1,{"answer":"Message received. Unsupported command"})
            Logger().error("Restart not yet implemented")
            raise NotImplementedError("Not Implemented")
        else:
            callback(self,1,{"answer":"Message received. Unsupported command"})
            Logger().error("Unsupported command '" + args['option'] + "'")
        
        #TODO: shutdown, restart
    
    
