from Plugin import *

class PowerManager(Plugin):
    '''The first example class for the python powered remote interface for my computer'''

    id = "power_manager"
    
    def __init__(self):
        Plugin.__init__(self)

    def run(self,callback,args):
        #args is a dictionary of commands and data
        #We can't do the callback after it is asleep/shutdown/etc.
        callback(self,0,{"answer":"Message recieved. Taking action...."})
        
        if args['option'] == 'sleep':
            os.system("osascript -e 'tell application \"System Events\" to sleep'")
        
        #TODO: shutdown, restart
    
    
