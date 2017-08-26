from pwn import *
from elftools.elf.elffile import ELFFile
from elftools.elf.sections import SymbolTableSection

f = open("WTF","rb")
k = f.read()
f.close()

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
print hex(fs)
if ord(k[fs]) == 0x68:
    size = u32(k[fs+1:fs+5])
elif ord(k[fs]) == 0x6a:
    size = ord(k[fs+1])

sp = modify_file +0x30
if ord(k[sp-1]) == 0x6a:
    patch = k[:sp] + chr(size) + k[sp+1:]
elif ord(k[sp-1]) == 0x68:
    patch = k[:sp] + p32(size) + k[sp+4:]

    
f = open("Patch","wb")
f.write(patch)
f.close()
