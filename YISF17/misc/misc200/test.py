from qrtools import QR
from PIL import Image
'''
f = open("fXXk","wb")
for i in range(1,1370):
    myCode = QR(filename=u"apngframe"+"0"*(4-len(str(i)))+str(i)+".png")
    if myCode.decode():
        f.write(myCode.data[61:]+"\n")
f.close()

MAP = [[2 for col in range(37)] for row in range(37)]
f = open("fXXk","rb")
K = f.read()
f.close()
T = K.split("\n")[:-1]
for p in T:
    if p.find("?") != -1:
        continue
    if p.find("Black") != -1:
        B = 1
    else:
        B = 0
    
    a = p.split(" ")
    MAP[int(a[0])][int(a[2])] = B
        
im = Image.new("RGB",(37,37))
pix = im.load()
for i in range(37):
    for j in range(37):
        if MAP[i][j] == 1:
            pix[i,j] = (0,0,0)
        elif MAP[i][j] == 0:
            pix[i,j] = (255,255,255)
        elif MAP[i][j] == 2:
            pix[i,j] = (0,0,0)
        else:
            pix[i,j] = (0,255,0)
im.save("WTF.png")
'''
i=13
myCode = QR(filename=u"WTF.png")
if myCode.decode():
    print(myCode.data+"\n")


