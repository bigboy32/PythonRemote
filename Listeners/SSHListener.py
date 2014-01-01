from Listener import Listener
import base64
from binascii import hexlify
import os
import socket
import sys
import threading
import traceback
import paramiko
from CreationExceptions import ListenerCreationException
from Utilities import *

import paramiko


class ParamikoServer(paramiko.ServerInterface):

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
        if (username == self.username) and (key == self.publickey):
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

    def get_allowed_auths(self, username):
        return 'password,publickey'

    def check_channel_shell_request(self, channel):
        self.event.set()
        return True

    def check_channel_pty_request(self, channel, term, width, height, pixelwidth, pixelheight, modes):
        return True

        
class SSHListener(Listener):
    '''An implementation of the listener class which listens for data using SSH.'''
    
    def __init__(self):
        Listener.__init__(self)
        self.privatekey = paramiko.RSAKey(filename='remote.key')
        Logger().info('Read key: ' + hexlify(self.privatekey.get_fingerprint()))
    
    def sendResponse(self, response):
        Logger().info("Responding")
        self.chan.send(str(response))
        
    def run(self, connectionFormed, commandReceived):

        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock.bind(('', 2200))
        except Exception, e:
            Logger().error('Bind failed: ' + str(e))
            traceback.print_exc()
            raise

        try:
            self.sock.listen(100)
            Logger().info('Listening for connection')
            client, addr = self.sock.accept()
        except Exception, e:
            Logger().error('Listen/accept failed: ' + str(e))
            traceback.print_exc()
            raise
        
        
        connectionFormed(self)

        try:
            self.transport = paramiko.Transport(client)
            try:
                self.transport.load_server_moduli()
            except:
                Logger().error('Failed to load moduli -- gex will be unsupported.')
                raise
            self.transport.add_server_key(self.privatekey)
            server = ParamikoServer()
            try:
                self.transport.start_server(server=server)
            except paramiko.SSHException, x:
                Logger().error('SSH negotiation failed.')
                sys.exit(1)

            # wait for auth
            self.chan = self.transport.accept(20)
            if self.chan is None:
                Logger().error('No channel.')
                raise Exception("No channel")
            
            Logger().info('Authenticated!')

            server.event.wait(10)

            self.chan.send('You are connected to the server. Send your commands.\r\n')
            command = ''
            f = self.chan.makefile('rU')
            while(True):
                command = f.readline().strip('\r\n')
                if command == 'quit':
                    break
                commandReceived(self,command)
                self.chan.send("Received command\r\n")
            self.chan.close()

        except Exception, e:
            Logger().error('Caught exception: ' + str(e.__class__) + ': ' + str(e))
            traceback.print_exc()
            try:
                self.transport.close()
            except:
                pass
            raise
        
    def quit(self):
        Logger().info("quitting")
        