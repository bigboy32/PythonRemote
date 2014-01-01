import platform

class SystemInfo(object):
    '''A class for easily accessing all system information'''
    
    @staticmethod
    def getOS():
        return platform.system()
    
    @staticmethod
    def isWindows():
        return SystemInfo.getOS() == "Windows"
    
    @staticmethod
    def isMac():
        return SystemInfo.getOS() == "Darwin"
    
    @staticmethod
    def isLinux():
        return SystemInfo.getOS() == "Linux"
    