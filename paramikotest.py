import base64
from binascii import hexlify
import os
import socket
import sys
import threading
import traceback

import paramiko


class Server (paramiko.ServerInterface):

    def __init__(self):
        self.publickey = 'AAAAB3NzaC1yc2EAAAADAQABAAABAQDhDyRaRUj11xjiTsWoeGFl5Nwj9mExkS+ewygltgBpAbiqBJm/7Slw43tHROvs0oNqiSee5lZNqHxV/m/uy8Xtd+BVIf/eWhvS8ySNk0hAwxJ5h9DVMTYag/ssXuRiPyml6u7BYW2PH6n7Zi6M0blhu59olXXTQTyR50nboQCvFG7q7TW7/stUhD/H4XuqD0GlEoV9l1iQxww+dX8fGHh+XSbTZLEJEG3fBQABEdocV7fdoE5t8lhnaC1a3i20rAReVSe7aYDpaZ9lPQh9WTHF260xcZ4qMybZASJ7vWzf9K9DEIChJ8bUu4Y1p9492BKAy16grIoK34glxmuYkIax'
        self.publickey = paramiko.RSAKey(data=base64.decodestring(self.publickey))
        self.username = "velox"
        self.password = "pass"
        self.event = threading.Event()

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
        if (username == self.username) and (password == self.password):
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

    def check_auth_publickey(self, username, key):
        print 'Auth attempt with key: ' + hexlify(key.get_fingerprint())
        if (username == 'robey') and (key == self.publickey):
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

    def get_allowed_auths(self, username):
        return 'password,publickey'

    def check_channel_shell_request(self, channel):
        self.event.set()
        return True

    def check_channel_pty_request(self, channel, term, width, height, pixelwidth, pixelheight, modes):
        return True

        
# setup logging

privatekey = paramiko.RSAKey(filename='remote')

print 'Read key: ' + hexlify(privatekey.get_fingerprint())


# now connect
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', 2200))
except Exception, e:
    print '*** Bind failed: ' + str(e)
    traceback.print_exc()
    sys.exit(1)

try:
    sock.listen(100)
    print 'Listening for connection ...'
    client, addr = sock.accept()
except Exception, e:
    print '*** Listen/accept failed: ' + str(e)
    traceback.print_exc()
    sys.exit(1)

print 'Got a connection!'

try:
    t = paramiko.Transport(client)
    try:
        t.load_server_moduli()
    except:
        print '(Failed to load moduli -- gex will be unsupported.)'
        raise
    t.add_server_key(privatekey)
    server = Server()
    try:
        t.start_server(server=server)
    except paramiko.SSHException, x:
        print '*** SSH negotiation failed.'
        sys.exit(1)

    # wait for auth
    chan = t.accept(20)
    if chan is None:
        print '*** No channel.'
        sys.exit(1)
    print 'Authenticated!'

    server.event.wait(10)
    if not server.event.isSet():
        print '*** Client never asked for a shell.'
        sys.exit(1)

    chan.send('\r\n\r\nWelcome to my dorky little BBS!\r\n\r\n')
    chan.send('We are on fire all the time! Hooray! Candy corn for everyone!\r\n')
    chan.send('Happy birthday to Robot Dave!\r\n\r\n')
    chan.send('Username: ')
    f = chan.makefile('rU')
    username = f.readline().strip('\r\n')
    chan.send('\r\nI don\'t like you, ' + username + '.\r\n')
    chan.close()

except Exception, e:
    print '*** Caught exception: ' + str(e.__class__) + ': ' + str(e)
    traceback.print_exc()
    try:
        t.close()
    except:
        pass
    sys.exit(1)