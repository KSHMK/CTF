from paddingoracle import BadPaddingException, PaddingOracle
from base64 import b64encode, b64decode
from urllib import quote, unquote
import requests
from pwn import *
import time

class PadBuster(PaddingOracle):
    def __init__(self, **kwargs):
        super(PadBuster, self).__init__(**kwargs)
        self.session = requests.Session()
        self.wait = kwargs.get('wait', 2.0)

    def oracle(self, data, **kwargs):
        somecookie = b64encode(data)

        r = remote('112.166.114.149',1337)
        r.sendlineafter("> ","2")
        r.sendlineafter(": ","guest")
        r.sendlineafter(": ","714d0ea3d35368817a2656a5884c722e")
        r.sendlineafter("> ","1")
        r.sendlineafter(": ","guest,{}".format(somecookie))
        K = r.recvuntil("> ")

        r.close()
        del r
        if K.find("invalid padding") == -1:
            logging.debug('No padding exception raised on %r', somecookie)
            return

        # An HTTP 500 error was returned, likely due to incorrect padding
        raise BadPaddingException

if __name__ == '__main__':
    import logging
    import sys

    if not sys.argv[1:]:
        print 'Usage: %s <somecookie value>' % (sys.argv[0], )
        sys.exit(1)

    logging.basicConfig(level=logging.DEBUG)

    encrypted_cookie = b64decode(unquote(sys.argv[1]))

    padbuster = PadBuster()

    cookie = padbuster.decrypt(encrypted_cookie, block_size=8, iv=bytearray(8))

    print('Decrypted somecookie: %s => %r' % (sys.argv[1], cookie))
