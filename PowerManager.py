import Plugin

class PowerManager(Plugin):
	'''The first example class for the python powered remote interface for my computer'''

	id = "power_manager"
	
	def __init__(self):
		Plugin.__init__(self)

	def run(self,callback,args):
		#args is a dictionary of commands and data
		print args
		#When complete run the callback so that we can notify whoever asked what happened		
		callback(self,0,"Message")
	
