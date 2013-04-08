import socket
import sys
 
HOST = 'localhost'
PORT = 22001
 
try:
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error, msg:
  sys.stderr.write("[ERROR] %s\n" % msg[1])
  sys.exit(1)
 
try:
  sock.connect((HOST, PORT))
except socket.error, msg:
  sys.stderr.write("[ERROR] %s\n" % msg[1])
  sys.exit(2)

print "Enter plugin name: ",
p = raw_input()
print "--------------"
print
k,v = raw_input(),raw_input()

message = "<plugin name=\"%s\">" % (p)
while True:
	if k == "quit":
		break
	message += "<param key=\"%s\">%s</param>" % (k,v)
	k,v = raw_input(),raw_input()
message += "</plugin>"
sock.send(message)
sock.close()
 
print string
 
sys.exit(0)