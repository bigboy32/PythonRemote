import platform

class Plugin(object):

    def __init__(self):
        self.os = platform.system()

    def getOS(self):
        return self.os
