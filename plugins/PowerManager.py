class PowerManager(object):
'''The first example class for the python powered remote interface for my computer'''

	id = "power_manager"
	
	def run(callback,args):
		#args is a dictionary of commands and data
		print args
		#When complete run the callback so that we can notify whoever asked what happened		
		callback(completion_code)
	