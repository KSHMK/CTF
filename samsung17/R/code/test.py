import socket
import json

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('longest-substr.eatpwnnosleep.com', 9000))

f = open("oh.cpp","rb")
code = f.read()
f.close()
a = {
    'apikey' : 'b21ac804b10c3448f6f77db33945d603eb1764a24fe1a2287c7adae2d041c66a',
    'probid' : 'longest-substr',
    'sourcetype' : 'cpp',
    'code' : code,
}

s.send(json.dumps(a))
print (s.recv(102400))
