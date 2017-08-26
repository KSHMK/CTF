from pwn import *

r = remote("bb8.chal.pwning.xxx",20811)
def GetQubit():
    Zq = []
    for i in range(600-1):
        print i
        r.sendlineafter("Bob, do you want to intercept (y/N)?","y")
        r.sendlineafter("(Z/Y)","Z")
        r.recvuntil("measured ")
        K = r.recvuntil("\n")
        Zq.append(int(K))
        r.sendlineafter("(Y)?","N")
        r.sendlineafter("(y/N)?","N")
    r.sendlineafter("Bob, do you want to intercept (y/N)?","y")
    r.sendlineafter("(Z/Y)","Z")
    r.recvuntil("measured ")
    K = r.recvuntil("\n")
    Zq.append(int(K))
    r.sendlineafter("(Y)?","N")
    return Zq
def WatchBases(Zq):
    Cq = []
    for i in range(600):
        print i,
        r.sendlineafter("(y/N)?","y")
        r.sendlineafter("(Z/Y)","Z")
        r.sendlineafter("(Y)?","Y")
        r.sendlineafter("(Z/Y)","Z")
        r.sendlineafter("(-1/1)","-1")
        r.sendlineafter("(y/N)?","y")
        r.sendlineafter("(Z/Y)","Z")
        r.recvuntil("measured ")
        K = r.recvuntil("\n")
        if int(K) == 1:
            Cq.append(Zq[i])
            print "F"
        r.sendlineafter("(Y)?","N")
    return Cq
def main():
    Zqubits = GetQubit()
    print Zqubits
    Cqubits = WatchBases(Zqubits)
    print Cqubits
    r.interactive()
if __name__ == "__main__":
    main()
