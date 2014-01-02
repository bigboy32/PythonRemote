import platform

class SystemInfo(object):
    '''A class for easily accessing all system information'''
    
    @staticmethod
    def get_OS():
        return platform.system()
    
    @staticmethod
    def is_windows():
        return SystemInfo.get_OS() == "Windows"
    
    @staticmethod
    def is_mac():
        return SystemInfo.get_OS() == "Darwin"
    
    @staticmethod
    def is_linux():
        return SystemInfo.get_OS() == "Linux"
    