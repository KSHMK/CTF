from pwn import *
from time import sleep

def Calcer(t1,t2,t3):
    if t1 == 04:
        return (t3+t2) & 0xff
    if t1 == 0x2c:
        return (t3-t2) & 0xff
    if t1 == 0xfe:
        if t2 == 0xc0:
            return (t3+1) & 0xff
        if t2 == 0xc8:
            return (t3-1) & 0xff
    if t1 == 0x34:
        return t3 ^ t2
    if t1 == 0xb0:
        return t2

context.arch = 'amd64'
r = remote("35.189.150.198",33333)
sleep(0.5)
r.recv(4096)
sleep(0.5)
r.recv(4096)
sleep(0.5)
for i in range(30):
    r.recv(4096)
    sleep(0.5)
    K = r.recv(4096)
    text = K[0x24]+K[0x2a]+K[0x31]+K[0x38]+K[0x3f]+K[0x46]+K[0x4d]+K[0x54]
    print text
    r.send(text)
print "Phase 2 ------------------"
for i in range(20):
    r.recv(4096)
    sleep(0.5)
    K = r.recv(4096)
    p1 = p64(u64(K[0x67:0x6f]) ^ 0x9090909090909090)
    print p1
    r.send(p1)
    continue
    T = ""
    for i in range(105):
        T += chr(ord(K[i+0x6f]) ^ ord(p1[i%8]))
    p2 = ""
    t = 0
    for i in range(8):
        print hex(ord(T[t+0])),hex(ord(T[t+1])),hex(ord(T[t+2])),hex(ord(T[t+3]))
        k = Calcer(ord(T[t]),ord(T[t+1]),0)
        k = Calcer(ord(T[t+2]),ord(T[t+3]),k)
        p2 += chr(k)
        if i == 0:
            t += 9
        else:
            t += 10
    print p1+p2
    
r.recv(4096)
sleep(0.5)
K = r.recv(4096)
f = open("LOL","wb")
f.write(K)
f.close()
