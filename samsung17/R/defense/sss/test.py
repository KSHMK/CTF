from pwn import *
import json
import base64

r = remote("sss.eatpwnnosleep.com", 18878)

a = {
    'apikey' : "b21ac804b10c3448f6f77db33945d603eb1764a24fe1a2287c7adae2d041c66a",
}
f = open("valenv.c","rb")
k = f.read()
f.close()
k = base64.b64encode(k)

r.sendline(json.dumps(a).encode())

r.sendline("valenv.c")
r.sendlineafter(" base64 :",k)

r.sendline("valenv.c")
r.sendlineafter(" base64 :",k)
r.interactive()

