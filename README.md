#PythonRemote
-----
PythonRemote is a python program which runs on your computer which remotes can connect to and allow you to send commands to your machine. The remotes will be plugable so that anyone can add remotes to it once I have an appropriate interface defined. 

##Authentication

###Planned Pairing Method

1. User starts "pair" operation in server
2. Server generates a public-private key pair and displays the private key as a QR code
3. User scans QR code using mobile app
4. Private key stored in mobile device keychain

###Planned Auth Method

Every device will be authenticated using the pairing method as above. The connection will be secured using the SSH protocol. Server side, this will be done using paramiko.

##Dependencies

* [Twisted](http://twistedmatrix.com/trac/wiki/Downloads)
