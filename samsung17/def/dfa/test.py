import base64
from pwn import *
r =  remote("dfa.eatpwnnosleep.com",9999)
r.sendlineafter("finish","auto.c")
f = open("auto_fix.c")
k= base64.b64encode(f.read())
f.close()
r.sendlineafter("base64 : ",k)
r.interactive()
