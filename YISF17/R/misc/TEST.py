'''
for i in range(777):
    k=["","",""]
    st = 0
    md = 0
    ed = 0
    for j in range(3):
        f = open(str(i+1)+"/"+str(j+1),"rb")
        k[j] = f.read()
        f.close()
        del f
        if k[j].find("PNG") != -1:
            st = j
        elif k[j].find("END") != -1:
            ed = j
        else:
            md = j
    f = open("PNG/"+str(i+1)+".png","wb")
    f.write(k[st]+k[md]+k[ed])
    f.close()
    del f
'''    
from PIL import Image
N = Image.new("RGB",(1554,777))
pix = N.load()
for i in range(777):
    im = Image.open("PNG/"+str(i+1)+".png")
    p = im.load()
    for j in range(777):
        pix[i*2,j] =p[0,j]
        pix[(i*2)+1,j] = p[1,j]
    im.close()
    del im
N.save("HMM.png")
