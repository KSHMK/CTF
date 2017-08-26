# -*- coding: utf-8 -*-
from paddingoracle import BadPaddingException, PaddingOracle
from base64 import b64encode, b64decode
from urllib import quote, unquote
import requests
import socket
import time


def ru(socket,until):
 string = ""
 while not until in string:
  string += socket.recv(1)
 return string


class PadBuster(PaddingOracle):
    def __init__(self, **kwargs):
        super(PadBuster, self).__init__(**kwargs)

    def oracle(self, data, **kwargs):
        fuck = str(data).encode("base64").replace("\n", "")
        # print fuck

        HOST = '112.166.114.149'
        PORT = 1337
        rem = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        rem.connect((HOST, PORT))

        rr = ru(rem, "> ")
        # print rr
        rem.send("2\n")
        rr = ru(rem, ": ")
        # print rr
        rem.send("guest\n")
        rr = ru(rem, ": ")
        # print rr
        rem.send("714d0ea3d35368817a2656a5884c722e\n")
        rr = ru(rem, "> ")
        # print rr
        rem.send("1\n")
        rr = ru(rem, ": ")
        # print rr
        rem.send("{},{}\n".format("guest", fuck))
        sex=ru(rem, "> ")
        # print sex

        rem.close()
        del rem
        # print sex

        if sex.find("invalid padding") == -1:
            return

        raise BadPaddingException()

if __name__ == '__main__':
    import logging
    import sys

    if not sys.argv[1:]:
        print 'Usage: %s <somecookie value>' % (sys.argv[0], )
        sys.exit(1)

    logging.basicConfig(level=logging.DEBUG)

    encrypted_cookie = b64decode(unquote(sys.argv[1]))

    padbuster = PadBuster()

    cookie = padbuster.decrypt(encrypted_cookie, block_size=16,
    iv=bytearray('\x7f\x7e\x7d\x7c\x7b\x7a\x79\x78'*2))

    print('Decrypted somecookie: %s => %r' % (sys.argv[1], cookie))
