# Embedded file name: final.py
import uuid
import socket
import httplib
import urllib
import urllib2
import os
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

f = open('flag_enc.txt', 'rb')
msg = f.read()
f.close()
f = open("p3.txt","rb")
p = f.read()
f.close()

key = RSA.importKey(p)
msg = key.decrypt(msg)
f = open('flag.txt', 'wb')
f.write(msg)
f.close()
