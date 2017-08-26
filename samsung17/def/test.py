from pwn import *
from elftools.elf.elffile import ELFFile
import base64
#SCTF{BAD_1s_B3y0ndAppleD3veloper}
r = remote("bad2.eatpwnnosleep.com", 8888)
r.recvuntil("STAGE : 1")
try:
    for i in range(30):
        log.info("Stage"+str(i+1))
        k = r.recvuntil("Send")[:-4]
        k = base64.b64decode(k)
        patch = ""
        fs = 0x713
        if ord(k[fs]) == 0x81:
            size = u32(k[fs+2:fs+6])-12
            sp = 0x71d
        elif ord(k[fs]) == 0x83:
            size = ord(k[fs+2])-12
            sp = 0x71a

        if ord(k[sp-1]) == 0x6a:
            patch = k[:sp] + chr(size) + k[sp+1:]
        elif ord(k[sp-1]) == 0x68:
            patch = k[:sp] + p32(size) + k[sp+4:]
        
        r.sendline(base64.b64encode(patch))

        r.recvuntil("Success!")
except EOFError :
    f = open("WTF","wb")
    f.write(k)
    f.close()
    f = open("Patch","wb")
    f.write(patch)
    f.close()
    
r.recvuntil("STAGE : 2")
try:
    for i in range(30):
        log.info("Stage"+str(i+1))
        k = r.recvuntil("Send")[:-4]
        k = base64.b64decode(k)

        f = open("WTF","wb")
        f.write(k)
        f.close
        f = open("WTF","rb")
        elffile = ELFFile(f)
        symtab = elffile.get_section_by_name(b'.symtab')
        for sym in symtab.iter_symbols():
            if sym.name == "get_file":
                get_file = sym['st_value'] - 0x8048000
            if sym.name == "get_int":
                get_int = sym['st_value'] - 0x8048000
        f.close()
        
        patch = ""
        fs = get_int+3
        if ord(k[fs]) == 0x81:
            size = u32(k[fs+2:fs+6])-12
            sp = get_int+0xd
        elif ord(k[fs]) == 0x83:
            size = ord(k[fs+2])-12
            sp = get_int+0xa

        if ord(k[sp-1]) == 0x6a:
            patch = k[:sp] + chr(size) + k[sp+1:]
        elif ord(k[sp-1]) == 0x68:
            patch = k[:sp] + p32(size) + k[sp+4:]

        k = patch
        fs = get_file+3
        if ord(k[fs]) == 0x81:
            size = u32(k[fs+2:fs+6])-12
            sp = get_file+0x1b
        elif ord(k[fs]) == 0x83:
            size = ord(k[fs+2])-12
            sp = get_file+0x18

        if ord(k[sp-1]) == 0x6a:
            patch = k[:sp] + chr(size) + k[sp+1:]
        elif ord(k[sp-1]) == 0x68:
            patch = k[:sp] + p32(size) + k[sp+4:]
        
            
        r.sendline(base64.b64encode(patch))

        r.recvuntil("Success!")
except EOFError :
    f = open("WTF","wb")
    f.write(k)
    f.close()
    f = open("Patch","wb")
    f.write(patch)
    f.close()

r.recvuntil("STAGE : 3")
try:
    for i in range(30):
        log.info("Stage"+str(i+1))
        k = r.recvuntil("Send")[:-4]
        k = base64.b64decode(k)

        f = open("WTF","wb")
        f.write(k)
        f.close
        f = open("WTF","rb")
        elffile = ELFFile(f)
        symtab = elffile.get_section_by_name(b'.symtab')
        for sym in symtab.iter_symbols():
            if sym.name == "get_file":
                get_file = sym['st_value'] - 0x8048000
            if sym.name == "get_int":
                get_int = sym['st_value'] - 0x8048000
            if sym.name == "modify_file":
                modify_file = sym['st_value'] - 0x8048000
            if sym.name == "create_file":
                create_file = sym['st_value'] - 0x8048000
        f.close()

        patch = ""
        fs = get_int+3
        if ord(k[fs]) == 0x81:
            size = u32(k[fs+2:fs+6])-12
            sp = get_int+0xd
        elif ord(k[fs]) == 0x83:
            size = ord(k[fs+2])-12
            sp = get_int+0xa

        if ord(k[sp-1]) == 0x6a:
            patch = k[:sp] + chr(size) + k[sp+1:]
        elif ord(k[sp-1]) == 0x68:
            patch = k[:sp] + p32(size) + k[sp+4:]

        k = patch
        fs = get_file+3
        if ord(k[fs]) == 0x81:
            size = u32(k[fs+2:fs+6])-12
            sp = get_file+0x1b
        elif ord(k[fs]) == 0x83:
            size = ord(k[fs+2])-12
            sp = get_file+0x18

        if ord(k[sp-1]) == 0x6a:
            patch = k[:sp] + chr(size) + k[sp+1:]
        elif ord(k[sp-1]) == 0x68:
            patch = k[:sp] + p32(size) + k[sp+4:]

        k = patch
        fs = k[create_file:].find("\x83\xC4\x10\x8B\x45\xF4\x83\xEC\x08")+9+create_file
        if ord(k[fs]) == 0x68:
            size = u32(k[fs+1:fs+5])
        elif ord(k[fs]) == 0x6a:
            size = ord(k[fs+1])

        sp = modify_file +0x30
        if ord(k[sp-1]) == 0x6a:
            patch = k[:sp] + chr(size) + k[sp+1:]
        elif ord(k[sp-1]) == 0x68:
            patch = k[:sp] + p32(size) + k[sp+4:]
        
            
        r.sendline(base64.b64encode(patch))

        r.recvuntil("Success!")
except EOFError :
    f = open("WTF","wb")
    f.write(k)
    f.close()
    f = open("Patch","wb")
    f.write(patch)
    f.close()
r.interactive()

