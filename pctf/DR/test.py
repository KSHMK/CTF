from z3 import *
v11 = []
for i in range(15):
    v11.append(BitVec("v"+str(i),8))
text = "PCTF{"
S = Solver()
for i in range(15):
    S.add(v11[i] >= 0x20,v11[i]<0x80)
T = "\x77\x5F\x57\x16\x4A\x59\x46\x16\x40\x53\x56\x16\x5A\x42\x0C\x00"
for i in range(5):
    if i & 1 == 1:
        v7 = v11[2] ^ v11[3] ^ v11[4] ^ v11[5] ^ ord(T[i]) ^ 0x73 
    else:
        v7 = v11[5] ^ v11[6] ^ v11[7] ^ v11[8] ^ v11[9] ^ ord(T[i]) ^ 0x31
    for k in range(15):
        v7 ^= v11[k]
    S.add(v7 == ord(text[i]))
print S.check()
print S.model()

