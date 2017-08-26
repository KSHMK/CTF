f = open("encoded_flaga.txt","rb")
K = f.read()
f.close()
ENC = [ord(x) ^ 0x34 for x in K]
flag = ""
n = 0
for i in range(5):
    flag += chr(ENC[i+n] - 0x10)
n+=5
for i in range(5):
    flag += chr(ENC[i+n] + 0x20)
n+=5
for i in range(5):
    flag += chr(ENC[i+n] / 0x2)
n+=5
for i in range(5):
    flag += chr(ENC[i+n] ^ 0xaa)

print flag
