from SystemInfo import SystemInfo
from Utilities import *

class Plugin(object):
    '''A base class for Plugin objects'''
    
    def run(self, callback, arguements):
        raise NotImplementedError("Not Implemented")
