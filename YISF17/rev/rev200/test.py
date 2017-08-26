from pwn import *
import os
import base64
import angr
import simuvex
from elftools.elf.elffile import ELFFile

def findKey():
    f = open("tmp","rb")
    elffile = ELFFile(f)

def main():
    r = remote("112.166.114.190", 19000)
    r.sendlineafter("are you ready? (y/n)","y")
    for i in range(1):
        print i
        r.recvuntil(".\n")
        k = r.recvuntil("input key:")
        f= open("tmp.7z","wb")
        f.write(base64.b64decode(k[1:-11]))
        f.close()
        os.system("7z x tmp.7z -y")
        key = findKey()
        r.sendline(key)
    r.interactive()

if __name__ == "__main__":
    main()
