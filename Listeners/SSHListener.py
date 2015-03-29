import base64
from binascii import hexlify
import os
import socket
import threading
import traceback

import paramiko
from paramiko import RSAKey

from Listener import Listener
from Utilities import *


class RSAKeygen(object):
    def generate(self):
        bits = 4096
        filename = "remote.key"

        # generating private key
        Logger().info("Generating key pair. This can take up to a minute.")
        prv = RSAKey.generate(bits=bits)
        prv.write_private_key_file(filename)
        Logger().info("Key pair generation complete.")

        # generating public key
        pub = RSAKey(filename=filename)
        with open("%s.pub" % filename, 'w') as f:
            f.write("%s %s" % (pub.get_name(), pub.get_base64()))

        hash = hexlify(pub.get_fingerprint())
        hex_hash = ":".join([hash[i:2 + i] for i in range(0, len(hash), 2)])
        Logger().info("Fingerprint: %d %s %s.pub (%s)" % (bits, hex_hash, filename, "RSA"))


class ParamikoServer(paramiko.ServerInterface):
    def __init__(self, username, password):
        with open('remote.key.pub') as f:
            pubkey = f.readlines()
        self.publickey = pubkey[0].replace('ssh-rsa ', '')
        self.publickey = paramiko.RSAKey(data=base64.decodestring(self.publickey))
        self.username = username
        self.password = password
        self.event = threading.Event()

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
        Logger().info("Checking username: " + username + " and password: " + password)
        if (username == self.username) and (password == self.password):
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

    def check_auth_publickey(self, username, key):
        print 'Auth attempt with key: ' + hexlify(key.get_fingerprint())
        if (username == self.username) and (key == self.publickey):
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

    def get_allowed_auths(self, username):
        if self.password == "":
            return 'publickey'
        else:
            return 'password,publickey'

    def check_channel_shell_request(self, channel):
        self.event.set()
        return True

    def check_channel_pty_request(self, channel, term, width, height, pixelwidth, pixelheight, modes):
        return True


class SSHListener(Listener):
    '''An implementation of the listener class which listens for data using SSH.'''

    def __init__(self, username="Velox", password=""):
        Listener.__init__(self)
        self.username = username
        self.password = password
        if not os.path.isfile("remote.key"):
            Logger().warning("No public key detected. Generating key pair.")
            kg = RSAKeygen()
            kg.generate()

        self.privatekey = paramiko.RSAKey(filename='remote.key')
        Logger().info('Read key: ' + hexlify(self.privatekey.get_fingerprint()))

    def sendResponse(self, response):
        Logger().info("Responding")
        self.chan.send(str(response))

    def initiate_connection(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock.bind(('', 2200))
        except Exception, e:
            Logger().error('Bind failed: ' + str(e))
            traceback.print_exc()
            raise

        try:
            self.sock.listen(1)
            Logger().info('Listening for connection')
            self.client, self.addr = self.sock.accept()
        except Exception, e:
            Logger().error('Listen/accept failed: ' + str(e))
            traceback.print_exc()
            raise

    def setup_transport(self):
        self.transport = paramiko.Transport(self.client)
        try:
            self.transport.load_server_moduli()
        except:
            Logger().error('Failed to load moduli -- gex will be unsupported.')
            raise
        self.transport.add_server_key(self.privatekey)
        self.server = ParamikoServer(self.username, self.password)
        try:
            self.transport.start_server(server=self.server)
        except paramiko.SSHException, x:
            Logger().error('SSH negotiation failed.')
            raise

    def run(self, connection_formed, command_received):

        self.initiate_connection()
        connection_formed(self)

        try:
            self.setup_transport()

            # wait for auth
            self.chan = self.transport.accept(20)
            if self.chan is None:
                Logger().error('Client error')
                self.close()
                return

            Logger().info('Authenticated!')

            self.server.event.wait(10)

            # self.chan.send('You are connected to the server. Send your commands.\r\n')
            command = ''
            f = self.chan.makefile('rU')
            while (True):
                command = f.readline().strip('\r').strip('\n')
                if command == 'quit' or command == '':
                    break
                command_received(self, command)
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

    def close(self):
        try:
            self.chan.close()
            self.transport.close()
        except:
            pass

    def quit(self):
        self.close()
        Logger().info("quitting")
        
