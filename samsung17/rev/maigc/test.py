T1 = [0x577402D733AA7E7,
0x69BFDBF76396DB95,
0x0BF4477DE78DF7CE1,
0x6496707F80B1999F]
T2 = [0x7D53,
      0x5A95,
      0x55A9,
      0x5171]
T3 = [0xB567,
      0xE3C5,
      0xEE19,
      0xFE4B]
from z3 import *
'''serial = BitVec("key",64)
v7 = []
for i in range(4):
    v7.append(((T1[i]*serial)>>64)&0xffffffffffffffff)
v7[0] = (((((serial - v7[0]) >> 1) + v7[0]) >> 14) * T2[0])&0xffffffffffffffff
v7[1] = (((((serial - v7[1]) >> 1) + v7[1]) >> 14) * T2[1])&0xffffffffffffffff
v7[2] = ((v7[2] >> 14) * T2[2])&0xffffffffffffffff
v7[3] = ((v7[3] >> 13) * T2[3])&0xffffffffffffffff
'''
v5 = 0
s = Solver()
tt = []
for i in range(4):
    tt.append(BitVec("tt"+str(i),16))
    s.add(tt[i]>0)
for i in range(4):
    v4 = tt[i]
    for j in range(4):
        if i != j:
            v4 = (v4*T3[j])
    v5 = (v4+v5)
print v5
s.add(v5 == 0xC41FC083535F81E8)

print s.check()
print s.model()
        
