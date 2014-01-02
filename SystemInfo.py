import platform

class SystemInfo(object):
    '''A class for easily accessing all system information'''
    
    @staticmethod
    def getOS():
        return platform.system()
    
    @staticmethod
    def is_windows():
        return SystemInfo.getOS() == "Windows"
    
    @staticmethod
    def is_mac():
        return SystemInfo.getOS() == "Darwin"
    
    @staticmethod
    def is_linux():
        return SystemInfo.getOS() == "Linux"
    