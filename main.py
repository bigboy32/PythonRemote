import PowerManager

def callback(plugin,code,message):
	print plugin
	print code
	print message

def main():
	p = PowerManager()
	p.run(callback,{'A':'Hello',2:'World'})




if __name__ == '__main__':
 	main() 
