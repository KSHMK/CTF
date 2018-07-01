f = open("dingdong","rb")
K = f.read()
f.close()
T = ""
for i in range(0,len(K),8):
    if K[i] == "\x75":
        T += "."
    elif K[i] == "\x7a":
        T += "j"
    elif K[i] == "\x7f":
        T += "f"
    elif K[i] == "\x84":
        T += "d"
    elif K[i] == "\x89":
        T += "k"
A = 0
B = 0
S_str = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_!"
FLAG = [ i for i in "qN7BuRx4rElDv84dgNaaNBanZf0HSHFjqOvbkFfgTRg3r"]
S_len = len(S_str)
S = [i for i in S_str]
IDX = [i for i in range(S_len)]
FR = 380
def WTF(fr):
    global A
    global B
    global IDX
    for i in range(fr):
        A = (A+1)%S_len
        B = (B+IDX[A]) % S_len
        IDX[A], IDX[B] = IDX[B], IDX[A]
    return S[IDX[(IDX[A] + IDX[B]) % S_len]]
def OHWHAT():
    global FLAG
    for i in range(len(FLAG)):
        t = WTF(1)
        idx2 = S.index(FLAG[i])
        idx1 = S.index(t)
        FLAG[i] = S[(idx1 ^ idx2)%S_len]
for i in range(len(T)):
    if T[i] == "f":
        tmp = WTF(102*FR)
        OHWHAT()
    elif T[i] == "j":
        tmp = WTF(106*FR)
        OHWHAT()
    elif T[i] == "k":
        tmp = WTF(107*FR)
        OHWHAT()
    elif T[i] == "d":
        tmp = WTF(100*FR)
        OHWHAT()
    FR += 20
print "".join(str(i) for i in FLAG)
