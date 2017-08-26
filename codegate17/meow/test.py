import string
import itertools
import hashlib

k25 = 0x0d ^ 0x55
k23 = 0x48 ^ 0x48
k18 = 0xf5 ^ 0x89
k39 = 0xaf ^ 0xe5
k01 = 0xba ^ 0xc9
k13 = 0xa7 ^ 0xc3

for k3 in range(32,0x80):
    k1 = k13 ^ k3
    k0 = k01 ^ k1
    k2 = k23 ^ k3
    k5 = k25 ^ k2
    k8 = k18 ^ k1
    k9 = k39 ^ k3

    p = 1
    for i in [k0,k1,k2,k5,k8,k9]:
        if chr(i) not in string.printable:
            p = 0
            break
    if p == 0:
        continue
    part1 = ''.join([chr(x) for x in [k0,k1,k2,k3]])
    part2 = chr(k5)
    part3 = chr(k8)+chr(k9)
    print "TEST: "+part1+"?"+part2+"??"+part3
    for word in itertools.product(string.printable,repeat=3):
        key = part1+word[0]+part2+word[1]+word[2]+part3
        if hashlib.md5(key).hexdigest() == "9f46a92422658f61a80ddee78e7db914":
            print "-------------------------------"
            print key
            print "-------------------------------"
            exit()
    
