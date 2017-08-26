import random
flag = "WHOAMI"
def deprocess_flag(infile):
    inf = open(infile,"rb")
    K = inf.read()
    
    K = K.replace("\x0d\x0a","\x0a")
    print len(K)/65000
    inf.close()
    flag = ""
    for i in range((len(K)/65000)):
        c=0
        for k in range(65000):
            c ^= ord(K[(i*65000)+k])
        flag += chr(c)
    print flag

def process_flag (outfile):
    with open(outfile,'w') as f:
        for x in flag:
            c = 0
            towrite = ''
            for i in range(65000 - 1):
                k = random.randint(0,127)
                c = c ^ k
                towrite += chr(k)

            f.write(towrite + chr(c ^ ord(x)))
    return

deprocess_flag("texta")
