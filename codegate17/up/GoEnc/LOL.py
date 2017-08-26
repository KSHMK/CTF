get 4 bytes
K = INPUT[:4]
for i in range(4,0x2d60,4):
	K[i] = K[i-4] ^ INPUT[i]
	K[i+1] = K[i-3] ^ INPUT[i+1]
	K[i+2] = K[i-2] ^ INPUT[i+2]
	K[i+3] = K[i-1] ^ INPUT[i+3]
P = "encryptk"
for i in range(0x2d60):
	K[i] ^= P[i%8]

for i in range(0,0x2d60,8):
	K[i], K[i+4] = K[i+4], K[i]
	K[i+1], K[i+5] = K[i+5], K[i+1]
	K[i+2], K[i+6] = K[i+6], K[i+2]
	K[i+3], K[i+7] = K[i+7], K[i+3]
j = 0x2d5f
for i in range(0,0x16af):
	K[j] ^= K[i]
	j-=1

for i in range(0x2d60):
	K[i] ^= P[i%4];