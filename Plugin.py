import platform

class Plugin(object):

	#Possible OS types:
		#Windows
		#

    def __init__(self):
        self.os = platform.system()

    def getOS(self):
        return self.os
