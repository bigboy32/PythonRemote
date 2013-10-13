#PythonRemote
-----
PythonRemote is a python program which runs on your computer which remotes can connect to and allow you to send commands to your machine. The remotes will be plugable so that anyone can add remotes to it once I have an appropriate interface defined. 

##Authentication

###Planned Pairing Method

1. User starts "pair" operation in server
2. Server generates a random password and displays it as a QR code
3. User scans QR code using mobile app
4. Password stored in mobile device keychain

###Planned Auth Method

All requests will pass a token which will be generated as:

`sha512(password + unixtime)` e.g. At 18:10:23PM on 13/10/2013 the token would be generated as: `sha512("mypassword" + "1381687823")` -> `7E5B03529965237BC578D4C829CC0B22F6B02F5870F8F267E73C842BD3FDF53A43433032FD9A59D1B92F106B52E2C3E49BC3632C1E4D15A06270C0CEC363EAE7`

Requests will be checked for X seconds before and after the sever time.

What value should X be?

###Notes

* With this method only one device will be able to control the server.
* Should I use a nonce instead of a timestamp to defeat replay attacks? It means the client will have to issue a nonce request before each command.

##Dependencies

* [Twisted](http://twistedmatrix.com/trac/wiki/Downloads)
