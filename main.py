from PowerManager import PowerManager
from Messager import *

def callback(plugin,code,values):
	print plugin
	print code
	print values

def main():
	p = Messager()
	print p.getOS()
	p.run(callback,{'type':'okcancel','title':'Message Title','message':'Hello World'})




if __name__ == '__main__':
 	main() 
