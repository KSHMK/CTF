''' NOT working :(
def LOL(sw):
    T = ""
    if (sw[1] & ( sw[2] | sw[4])):
        T += "1"
    else:
        T += "0"
    
    if (sw[3] ^ ( ( sw[1] | sw [4]) | ( ( (sw[2] & sw[5]) | (not sw[2] & (not sw[5])))))):
        T += "1"
    else:
        T += "0"

    if ((((sw[4] & sw[5]) | ((not sw[4]) & (not sw[5]))) | (not sw[2])) ^ sw[3]):
        T += "1"
    else:
        T += "0"
    
    if (sw[3] ^ ((not sw[4]) | (sw[2] | sw[5]))):
        T += "1"
    else:
        T += "0"
    
    if ((((sw[4] & (not sw[5])) | sw[1]) | ((((not sw[2]) & (not sw[5])) | ((not sw[2]) & sw[4])) | (sw[5] & (sw[2] & (not sw[4]))))) ^ sw[3]):
        T += "1"
    else:
        T += "0"
    
    if (((not sw[5] & sw[4]) | ((not sw[2]) & (not sw[5]))) ^ sw[3]):
        T += "1"
    else:
        T += "0"
    
    if ((((((not sw[4]) & (not sw[5])) | (sw[2] & (not sw[4]))) | ((not sw[5]) & sw[2])) | sw[1]) ^ sw[3]):
        T += "1"
    else:
        T += "0"
    
    if ((((sw[2] & (not sw[4])) | sw[1]) | (((not sw[2]) & sw[4]) | ((not sw[5]) & sw[4]))) ^ sw[3]):
        T += "1"
    else:
        T += "0"
    return T
'''
def LOL2(sw):
    T = ""
    c25400 = sw[1]
    c180254 = sw[2]
    c62540 = sw[3]
    c2542330 = sw[4]
    c0254251 = sw[5]
    c154156229 = not c180254
    c22866215 = c180254 | c2542330
    c227229154 = not c2542330
    c154229227 = not c0254251
    c75115119 = c2542330 & c0254251
    c213887 = c0254251 & c180254
    c124165127 = c154229227 & c227229154
    c148319 = c180254 & c154229227
    c872153 = c154156229 & c154229227
    c136100159 = c25400 & c22866215
    c16912247 = c180254 & c227229154
    c4716967 = c2542330 & c154156229
    c134779 = c0254251 & c16912247
    c255255255 = c2542330 & c154229227
    if c136100159:
        T+="1"
    else:
        T+="0"
    if (c62540 ^ ((c213887 | c872153) | (c2542330 | c25400))):
        T+="1"
    else:
        T+="0"
    if (c62540 ^ (c154156229 | (c75115119 | c124165127))):
        T+="1"
    else:
        T+="0"
    if (c62540 ^ (c227229154 | ( c0254251 | c180254))):
        T+="1"
    else:
        T+="0"
    if (c62540 ^ ((c25400 | c255255255) | ((c134779 | (c4716967 | c872153))))):
        T+="1"
    else:
        T+="0"
    if (c62540 ^ (c255255255 | c872153)):
        T+="1"
    else:
        T+="0"
    if (c62540 ^ (c25400 | ((c16912247 | c124165127) | c148319))):
        T+="1"
    else:
        T+="0"
    if (c62540 ^ ((c25400 | c16912247) | (c255255255 | c4716967))):
        T+="1"
    else:
        T+="0"
    return T
F = False
T = True
print LOL2([F,F,F,F,F,F]),"A"
print LOL2([F,F,F,F,F,T]),"B"
print LOL2([F,F,F,F,T,F]),"C"
print LOL2([F,F,F,F,T,T]),"D"
print LOL2([F,F,F,T,F,F]),"E"
print LOL2([F,F,F,T,F,T]),"F"
print LOL2([F,F,F,T,T,F]),"G"
print LOL2([F,F,F,T,T,T]),"H"
print LOL2([F,F,T,F,F,F]),"I"
print LOL2([F,F,T,F,F,T]),"J"
print LOL2([F,F,T,F,T,F]),"K"
print LOL2([F,F,T,F,T,T]),"L"
print LOL2([F,F,T,T,F,F]),"M"
print LOL2([F,F,T,T,F,T]),"N"
print LOL2([F,F,T,T,T,F]),"O"
print LOL2([F,F,T,T,T,T]),"P"
print LOL2([F,T,F,F,F,F]),"Q"
print LOL2([F,T,F,F,F,T]),"R"
print LOL2([F,T,F,F,T,F]),"S"
print LOL2([F,T,F,F,T,T]),"T"
print LOL2([F,T,F,T,F,F]),"U"
print LOL2([F,T,F,T,F,T]),"V"
print LOL2([F,T,F,T,T,F]),"W"
print LOL2([F,T,F,T,T,T]),"X"
print LOL2([F,T,T,F,F,F]),"Y"
print LOL2([F,T,T,F,F,T]),"Z"
print LOL2([F,T,T,F,T,F]),"?"
print LOL2([F,T,T,F,T,T]),"?"
print LOL2([F,T,T,T,F,F]),"?"
print LOL2([F,T,T,T,F,T]),"?"
print LOL2([F,T,T,T,T,F]),"?"
print LOL2([F,T,T,T,T,T]),"?"

