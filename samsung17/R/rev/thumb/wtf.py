def _int32(x):
    # Get the 32 least significant bits.
    return int(0xFFFFFFFF & x)

class MT19937:
    def __init__(self, seed):
        # Initialize the index to 0
        self.index = 624
        self.mt = [0] * 624
        self.mt[0] = seed  # Initialize the initial state to the seed
        for i in range(1, 624):
            self.mt[i] = _int32(
                1812433253 * (self.mt[i - 1] ^ self.mt[i - 1] >> 30) + i)

    def extract_number(self):
        if self.index >= 624:
            self.twist()

        y = self.mt[self.index]

        # Right shift by 11 bits
        y = y ^ y >> 11
        # Shift y left by 7 and take the bitwise and of 2636928640
        y = y ^ y << 7 & 2636928640
        # Shift y left by 15 and take the bitwise and of y and 4022730752
        y = y ^ y << 15 & 4022730752
        # Right shift by 18 bits
        y = y ^ y >> 18

        self.index = self.index + 1

        return _int32(y)

    def twist(self):
        for i in range(624):
            # Get the most significant bit and add it to the less significant
            # bits of the next number
            y = _int32((self.mt[i] & 0x80000000) +
                       (self.mt[(i + 1) % 624] & 0x7fffffff))
            self.mt[i] = self.mt[(i + 397) % 624] ^ y >> 1

            if y % 2 != 0:
                self.mt[i] = self.mt[i] ^ 0x9908b0df
        self.index = 0
        #test
def ROL(data, shift, size=128):
    shift %= size
    remains = data >> (size - shift)
    body = (data << shift) - (remains << size )
    return (body + remains)



TABLE = [[0 for col in range(16)] for row in range(16)]
RANDTABLE = []
LOL = MT19937(0xc0ffee)
TOTAL = 256 + (34*2) + (1000 * 2) + (1000 * 2) + (1000 * 3) + (1000 * 2)
for i in range(TOTAL):
    RANDTABLE.append(LOL.extract_number())
K = len(RANDTABLE)-1
f = open("TABLE1","rb")
t = f.read()
f.close()
for i in range(16):
    for j in range(16):
        TABLE[i][j] = ord(t[16*i+j])
for n in range(1000):
    a2 = RANDTABLE[K] & 0xf
    K-=1
    a1 = RANDTABLE[K] & 0xf
    K-=1
    for i in range(16):
        a = TABLE[i][a1]
        TABLE[i][a1] = TABLE[i][a2]
        TABLE[i][a2] = a

for n in range(1000):
    a3 = RANDTABLE[K] & 0xff
    K-=1
    a2 = RANDTABLE[K] & 0xf
    K-=1
    a1 = RANDTABLE[K] & 0xf
    K-=1
    for i in range(16):
        TABLE[i][a2] ^= a3
        TABLE[a1][i] ^= a3

for n in range(1000):
    a2 = RANDTABLE[K] & 0x7
    K-=1
    a1 = RANDTABLE[K] & 0xf
    K-=1
    v4 = 0
    for i in range(16):
        v4 *= 0x100
        v4 += TABLE[a1][i]
    v4 = ROL(v4,a2)
    for i in range(15,-1,-1):
        TABLE[a1][i] = v4 % 0x100
        v4 /= 0x100
f = open("hex2","wb")
for i in range(16):
    for j in range(16):
        f.write(chr(TABLE[i][j]))
f.close()


for n in range(1000):
    a2 = RANDTABLE[K] & 0xf
    K-=1
    a1 = RANDTABLE[K] & 0xf
    K-=1
    for i in range(16):
        a = TABLE[a1][i]
        TABLE[a1][i] = TABLE[a2][i]
        TABLE[a2][i] = a

f = open("hex2","wb")
for i in range(16):
    for j in range(16):
        f.write(chr(TABLE[i][j]))
f.close()

T = 0
for i in range(16):
    for j in range(16):
        TABLE[i][j] ^= RANDTABLE[T] & 0xff
        T+=1
print TABLE
flag = ""
for i in range(34):
    a1 = RANDTABLE[T] & 0xf
    T+=1
    a2 = RANDTABLE[T] & 0xf
    T+=1
    flag += chr(TABLE[a1][a2])
print flag
#SCTF{t1ny_tIny_baremetal_firmware}
