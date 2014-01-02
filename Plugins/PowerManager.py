from Plugin import *
from SystemInfo import *
import os

class PowerManager(Plugin):
    '''The first example class for the python powered remote interface for my computer'''

    id = "power_manager"
    
    def __init__(self):
        Plugin.__init__(self)

    def run(self,callback,args):
        #args is a dictionary of commands and data
        
        if args['option'] in ['sleep','hibernate']:
            if SystemInfo.is_mac():
                callback(self,0,None)
                os.system("osascript -e 'tell application \"System Events\" to sleep'")
            elif SystemInfo.is_windows():
                callback(self,0,None)
                os.system(r'%windir%\system32\rundll32.exe powrprof.dll,SetSuspendState Hibernate')
            else:
                callback(self,1,None)
                Logger().error("Unsupported OS for command 'sleep'")
        elif args['option'] == 'shutdown':
            callback(self,1,None)
            Logger().error("Shutdown not yet implemented")
            raise NotImplementedError("Not Implemented")
        elif args['option'] == 'restart':
            callback(self,1,None)
            Logger().error("Restart not yet implemented")
            raise NotImplementedError("Not Implemented")
        else:
            callback(self,1,None)
            Logger().error("Unsupported command '" + args['option'] + "'")
        
    