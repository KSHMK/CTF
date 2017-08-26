import base64
f = open("login.html","rb")
k = f.read()
f.close()
f = open("logout.php","wb")
f.write(base64.b64decode(k))
f.close()
