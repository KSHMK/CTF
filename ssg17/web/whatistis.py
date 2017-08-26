from Crypto.Cipher import AES
import base64

AES.key_size=128
iv="45c7f14c5f3642ac442705b956048ed0".decode('hex')
key="dd2d3b6473837ca33eaa61c390905c4f".decode('hex')
crypt_object=AES.new(key=key,mode=AES.MODE_CBC,IV=iv)

plain="WgYwiRujLBjnzoDYaSV7xHmZqn66qTNrDjEFfNl7NJRyMVbgRPpIKQt0tdx48rzZ"
decoded=base64.b64decode(plain) # your ecrypted and encoded text goes here
decrypted=crypt_object.decrypt(decoded)
print base64.b64encode(crypt_object.encrypt(decrypted))
print decrypted
