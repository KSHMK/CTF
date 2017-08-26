import string
import base64

my_base64chars  = "|yt2QGYA u  CeD0H/c)=NWVo&6nPk9$~dOKa?:<w8  !f  p Bxzl@s j   S  5"
std_base64chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
s = "=ze=/<fQCGSNVzfDnlk$&?N3oxQp)K/CVzpznK?NeYPx0sz5"
s = s.translate(string.maketrans(my_base64chars, std_base64chars))
print s
data = base64.b64decode(s)
print data
