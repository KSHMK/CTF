from Crypto.Cipher import AES

f = open("eggyolk","rb")
k = f.read()
f.close()

dec = AES.new("awesomecipherkey",AES.MODE_CBC,"handsomeinitvect")
f = open("eggs","wb")
f.write(dec.decrypt(k))
f.close()
