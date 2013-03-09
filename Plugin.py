import platform

class Plugin(object):

    def __init__(self):
        self.os = platform.sysem()

    def getOS(self):
        return self.os
