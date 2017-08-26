from pwn import *

r = remote("bb8.chal.pwning.xxx",20811)

def GetQubit():
    ZAq = []
    ZBq = []
    for i in range(599):
        print i
        r.sendlineafter("Bob, do you want to intercept (y/N)?","y")
        r.sendlineafter("(Z/Y)","Z")
        r.recvuntil("measured ")
        K = r.recvuntil("\n")
        ZAq.append(int(K))
        r.sendlineafter("(Y)?","Y")
        r.sendlineafter("(Z/Y)","Z")
        r.sendlineafter("(-1/1)","-1")
        ZBq.append(0)
        r.sendlineafter("(y/N)?","N")

    print "600"
    r.sendlineafter("Bob, do you want to intercept (y/N)?","y")
    r.sendlineafter("(Z/Y)","Z")
    r.recvuntil("measured ")
    K = r.recvuntil("\n")
    ZAq.append(int(K))
    r.sendlineafter("(Y)?","Y")
    r.sendlineafter("(Z/Y)","Z")
    ZBq.append(0)
    r.sendlineafter("(-1/1)","-1")
    return (ZAq,ZBq)

def WatchBases(ZAq,ZBq):
    CAq = []
    CBq = []
    C = 0
    T = 0
    for i in range(600):
        print i
        r.sendlineafter("(y/N)?","y")
        r.sendlineafter("(Z/Y)","Z")
        r.recvuntil("measured ")
        B = r.recvuntil("\n")
        r.sendlineafter("(Y)?","Y")
        r.sendlineafter("(Z/Y)","Z")
        r.sendlineafter("(-1/1)","-1")
        r.sendlineafter("(y/N)?","y")
        r.sendlineafter("(Z/Y)","Z")
        r.recvuntil("measured ")
        K = r.recvuntil("\n")
        if int(K) == 1:
            CAq.append(ZAq[i])
            C+=1
        r.sendlineafter("(Y)?","Y")
        r.sendlineafter("(Z/Y)","Z")
        if T <= 256:
            
            if int(B) == 1 or C == 0:
                r.sendlineafter("(-1/1)","-1")
            else:
                T+=1
                r.sendlineafter("(-1/1)","1")
                CBq.append(ZBq[i])
                C -= 1
        else:
            if C != 0:
                r.sendlineafter("(-1/1)","1")
                CBq.append(ZBq[i])
                C -= 1
            else:
                r.sendlineafter("(-1/1)","-1")
    return (CAq,CBq)

def Check(Cq):
    for i in range(0, len(Cq), 2):
        print i
        r.sendlineafter("(y/N)?", "y")
        r.sendlineafter("(Z/Y)","Z")
        r.sendlineafter("(Y)?","Y")
        r.sendlineafter("(Z/Y)","Z")
        r.sendlineafter("(-1/1)",str(Cq[i]))
        r.sendlineafter("(y/N)?","y")
        r.sendlineafter("(Z/Y)","Z")
        r.recvuntil("measured ")
        K = r.recvuntil("\n")
        if int(K) != 1:
            print "fuck!"
        r.sendlineafter("(Y)?","N")

def main():
    ZAq,ZBq = GetQubit()
    print ZAq
    print ZBq
    CAq,CBq = WatchBases(ZAq,ZBq)
    print CAq
    print CBq
    print len(CAq)
    print len(CBq)
    assert(len(CAq) == len(CBq))
    Check(CAq)

    KeybitsA = []
    KeybitsB = []

    for i in range(len(CAq)):
        if CAq[i] == -1:
            KeybitsA.append(0)
        else:
            KeybitsA.append(1)

    for i in range(len(CBq)):
        if CBq[i] == -1:
            KeybitsB.append(0)
        else:
            KeybitsB.append(1)

    print KeybitsA
    print KeybitsB
    aes_keyA = 0
    aes_keyB = 0
    for i in range(128):
        aes_keyA |= (KeybitsA[2*i+1] << (127-i))
        aes_keyB |= (KeybitsB[2*i+1] << (127-i))

    print "aes key A : " + hex(aes_keyA)
    print "aes key B : " + hex(aes_keyB)

    r.interactive()

if __name__ == "__main__":
    main()
