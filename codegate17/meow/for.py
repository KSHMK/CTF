import itertools
import string
import time
import hashlib
t = 0
sp = time.time()
for i in string.printable:
    for j in string.printable:
        for k in string.printable:
            for l in string.printable:
                t = hashlib.md5(i+j+k+l)
ep = time.time()
print "FOR: "+str(ep-sp)
sp = time.time()
for word in itertools.product(string.printable,repeat=4):
    t = hashlib.md5(word[0]+word[1]+word[2]+word[3])
ep = time.time()
print "ITR: "+str(ep-sp)
