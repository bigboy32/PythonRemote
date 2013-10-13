from SystemInfo import SystemInfo

class Plugin(object):
    '''A base class for Plugin objects'''
    
    def run(self, callback, arguements):
        raise NotImplementedError("Not Implemented")
