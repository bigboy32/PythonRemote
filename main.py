from PowerManager import PowerManager

def callback(plugin,code,values):
	print plugin
	print code
	print values

def main():
	p = PowerManager()
	p.run(callback,{'A':'Hello',2:'World'})




if __name__ == '__main__':
 	main() 
