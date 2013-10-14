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

All requests will send a request to the server of the form:

`{'authenticate':'device_id'}` 

The server will generate some random data and encrypt it with the public key. The data will be sent back to the client in the form:

`{'device':'device_id','data':'base_64_encrypted_data','valid':'unix_time_key_valid_to'}`

The app decrypts the data with its private key, and stores this as an auth token in the key chain.

From here all requests must use this token until it expires. Requests will be of the form:

`{'token':calculate_token,'nonce':'sha(base_64_token + unixtime)','name':'messager','type':'sync'}`

The calculate_token is `private_encrypt(auth_token + unixtime)`

Requests will be checked for X seconds before and after the sever time.

What value should X be?

###Notes

* With this method only one device will be able to control the server.
* Should I use a nonce instead of a timestamp to defeat replay attacks? It means the client will have to issue a nonce request before each command.

##Dependencies

* [Twisted](http://twistedmatrix.com/trac/wiki/Downloads)
