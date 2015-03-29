import socket
import sys
import json
import time

# This can be emulated: echo '{"name":"power_manager","type":"sync","data":{"option":"sleep"}}' | nc localhost 22001

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

if len(sys.argv) > 1 and sys.argv[1] == 'test':
    p = {'name': 'messager', 'type': 'sync',
         'data': {'title': 'test title', 'message': 'This is a test message', 'type': 'ok'}}
    sock.send(json.dumps(p))
    time.sleep(0.2)
    p = {'name': 'quit', 'type': 'sync'}
else:
    print "Enter plugin name: ",
    p = {'name': raw_input(), 'type': 'sync'}
    print "--------------"
    print
    k, v = raw_input(), raw_input()

    params = {}

    while True:
        if k == "quit":
            break
        params[k] = v
        k, v = raw_input(), raw_input()
    p['data'] = params

sock.send(json.dumps(p))

sock.close()

sys.exit(0)