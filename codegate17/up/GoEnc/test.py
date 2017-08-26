f = open("flaga.encrypt","rb")
INPUT = f.read()
f.close()
P = "encryptk"
K = []
for i in range(0x2d60):
    K.append(ord(INPUT[i]) ^ ord(P[i%4]))
j = 0x2d5f
for i in range(0,0x16af):
    K[j] ^= K[i]
    j-=1

for i in range(0,0x2d60,8):
    K[i], K[i+4] = K[i+4], K[i]
    K[i+1], K[i+5] = K[i+5], K[i+1]
    K[i+2], K[i+6] = K[i+6], K[i+2]
    K[i+3], K[i+7] = K[i+7], K[i+3]

P = "encryptk"
for i in range(0x2d60):
    K[i] ^= ord(P[i%8])

FLAG = "".join(chr(K[i]) for i in range(4))
for i in range(4,0x2d60,4):
    FLAG += chr(K[i] ^ K[i-4])
    FLAG += chr(K[i+1] ^ K[i-3])
    FLAG += chr(K[i+2] ^ K[i-2])
    FLAG += chr(K[i+3] ^ K[i-1])
f = open("flag.txt","wb")
f.write(FLAG)
f.close()
