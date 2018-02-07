from ctypes import CDLL
libc = CDLL("libc.so.6")

f = open("RESULT","rb")
COMP = f.read()
f.close()
f = open("sbox","rb")
SBOX = f.read()
f.close()
k = 0
DECOMP = ""
while True:
    if len(COMP) == k:
        break
    if ord(COMP[k]) == 0x16:
        l = SBOX.find(COMP[k+1])
        c = ord(COMP[k+2]) - (libc.rand() & 0xff)
        k+=3
        DECOMP += str(c) * l
    else:
        c = ord(COMP[k]) - (libc.rand() & 0xff)
        k+=1
        DECOMP += str(c)
print DECOMP
DECOMP = "10001000"
LEN = len(DECOMP)
C0 = 0
for i in DECOMP:
    if i == "0":
        C0 += 1
print C0
RORTABLE = ["" for i in range(LEN)]
for i in range(LEN):
    if C0 != 0:
        RORTABLE[i]="0"+"0"*(LEN-2)+DECOMP[i]
        C0 -= 1
    else:
        RORTABLE[i]="1"+"0"*(LEN-2)+DECOMP[i]
for i in range(LEN-2):
    for i in range(LEN):
        RORTABLE[i] = RORTABLE[i][-1]+RORTABLE[i][:-1]
    RORTABLE = sorted(RORTABLE)
    for i in range(LEN):
        RORTABLE[i] = RORTABLE[i][:-1]+DECOMP[i]
print RORTABLE[0]
print (hex(int(RORTABLE[0],2))[2:-1]+"0").decode('hex')
