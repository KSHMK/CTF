from Crypto.Cipher import AES
import glob
import os

ABS_PATH = '/home/flag/'

BLOCK_SIZE = 16

CORRECT_PADDING = 0
WRONG_BLOCK_LENGTH = 1
WRONG_PADDING_LENGTH = 2
WRONG_PADDING = 3

def ReadFile(file_path):
    try:
        f = open(file_path, 'rb')
        content = f.read()
        f.close()
        return content
    except:
        exit()

def WriteFile(file_path, content):
    try:
        f = open(file_path, 'wb')
        f.write(content)
        f.close()
    except:
        exit()

def InputNumber():
    try:
        num = int(raw_input('> ')) 
    except:
        num = -1
    return num

def Pad(s):
    padding = (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
    return s + padding

def Unpad(s):
    return s[:-ord(s[-1])]

def AESEncrypt(msg):
    try:
        msg = Pad(msg)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return cipher.encrypt(msg).encode('base64').replace('\n', '')
    except:
        return -1

def AESDecrypt(enc):
    try:
        enc = enc.decode('base64')
        cipher = AES.new(key, AES.MODE_CBC, iv)
        dec = cipher.decrypt(enc)
        s = CheckPadding(dec)
        if ( s != CORRECT_PADDING ):
            return s
        else:
            return Unpad(dec)
    except:
        return -1

def CheckPadding(s):
    if ( len(s) % BLOCK_SIZE != 0 ):
        return WRONG_BLOCK_LENGTH

    padding_length = ord(s[-1])

    if ( padding_length == 0 or padding_length > BLOCK_SIZE ):
        return WRONG_PADDING_LENGTH

    orig_padding = chr(padding_length) * padding_length
    s_padding = s[-padding_length:]

    if ( s_padding != orig_padding ):
        return WRONG_PADDING

    return CORRECT_PADDING

def StartSession(id):
    session = cookie1 + id + cookie2 + id + cookie3
    WriteFile(ABS_PATH + 'session/' + session, id)
    return AESEncrypt(session)

def FindSessionById(id):
    session = ''
    sessions = glob.glob(ABS_PATH + 'session/*')
    for c in sessions:
        if ( id == ReadFile(c) ):
            session = c[len(ABS_PATH + 'session/'):]
            break
    return session

key = ReadFile('key')
iv = '\x7f\x7e\x7d\x7c\x7b\x7a\x79\x78'*2
cookie1 = ReadFile('cookie1')
cookie2 = ReadFile('cookie2')
cookie3 = ReadFile('cookie3')

