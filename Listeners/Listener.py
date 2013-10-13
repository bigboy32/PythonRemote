from SystemInfo import SystemInfo

class Listener(object):
    '''A base class for all listener objects'''
    
    def run(self, connectionFormed, commandReceived):
        raise NotImplementedError("Not Implemented")
        
    def sendResponse(self, response):
        raise NotImplementedError("Not Implemented")

    def quit(self):
        raise NotImplementedError("Not Implemented")