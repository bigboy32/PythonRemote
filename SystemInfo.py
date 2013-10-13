import platform

class SystemInfo(object):
    '''A class for easily accessing all system information'''
    
    @staticmethod
    def getOS():
        return platform.system()