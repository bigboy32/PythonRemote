from Plugin import Plugin
from Tkinter import *
import tkMessageBox



class Messager(Plugin):
	'''Allows messages to be recieved and displayed to the current user'''

	id = "messager"
	
	def __init__(self):
		Plugin.__init__(self)

	def run(self,callback,args):
		#Arguments should have a 'type' key which can be any of:
		# 'abortretryignore','ok','okcancel','retrycancel','yesno','yesnocancel'
		if self.os in ["Windows","Darwin"]:
			window = Tk()
			window.wm_withdraw()
			#center the window on the main screen
			window.geometry("1x1+"+str(window.winfo_screenwidth()/2)+"+"+str(window.winfo_screenheight()/2))
			answer = tkMessageBox._show(type=args['type'],title=args['title'], message=args['message'],icon=None,)
			callback(self,0,{'answer':answer})
		else:
			sys.stderr.write('Unsupported OS for plugin "Messager"\n')
	
