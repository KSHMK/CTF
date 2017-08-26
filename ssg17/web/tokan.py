import base64
token = "userid_access_login_userid=ADMIN"
for i in range(4):
    token = base64.b64encode(token)
print token
for i in range(4):
    token = base64.b64decode(token)
print token
