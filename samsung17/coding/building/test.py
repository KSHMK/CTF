from pwn import *
from base64 import b64decode
from subprocess import Popen, PIPE, STDOUT
import hashlib
r = remote("buildingblocks.eatpwnnosleep.com", 46115)
for i in range(10):
    r.recvuntil("[")
    k = r.recvuntil("]")[:-1]
    k = k.replace("'","")
    k = k.split(", ")

    print k
    print "========================"
    sp = 0
    ep = 0

    proc = []
    flag = []
    for i,t in enumerate(k):
        proc.append(b64decode(t))
        if proc[i][0] == '\xb8':
            sp = i
            flag.append(0)
            continue
        if proc[i][-2:] == "\x0f\x05":
            ep = i
        flag.append(u32(proc[i][1:5]))
    patch = ""
    p = sp
    EAX = 0
    print flag
    print "sp : "+str(sp)+" ep : "+str(ep)
    while p != ep:
        patch += proc[p]
        print str(p)+" : "+proc[p].encode('hex')
        print str(EAX)+" "+str(len(proc[p]))
        pip = Popen(['./test', str(EAX), str(len(proc[p]))], stdin=PIPE, stdout=PIPE)
        pip.stdin.write(proc[p])
        pip.stdin.close()
        pip.wait()
        EAX  = int(pip.stdout.readline())
        print "RET "+str(EAX)
        p = flag.index(EAX)
    patch += proc[ep]
    r.sendline(hashlib.sha256(patch).hexdigest())
r.interactive()
