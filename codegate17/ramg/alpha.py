K = "47459\x00"
T = "MVYLXYUARJlu"
key = ""
for i in range(5):
    key += chr(ord(T[i]) ^ ord(K[i + (-5 * (i/5))]))
print key
T = "[S[X]DWYJ^lu3674231096"
K = "3674231096"
key = ""
for i in range(5):
    key += chr(ord(T[i]) ^ ord(K[i + (-10 * (i/10))]))
print key

