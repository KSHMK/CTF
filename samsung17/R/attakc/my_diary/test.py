from pwn import *
import json


r = remote("my_diary.eatpwnnosleep.com", 18879)

a = {
    'apikey' : "b21ac804b10c3448f6f77db33945d603eb1764a24fe1a2287c7adae2d041c66a",
}

r.send(json.dumps(a).encode())
r.recvuntil("verifed.\n")
r.interactive()

