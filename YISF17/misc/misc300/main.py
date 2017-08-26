#!/usr/bin/python
import sys
from etc import *

MENU_SEE_FLAG = 1
MENU_LOGIN = 2
MENU_CHANGE_SESSION = 3
MENU_QUIT = 4

def SeeFlag():
    if ( is_logged_in == False ):
        print 'login first plz :)'
        return

    tmp = raw_input('input id again plz: ')
    cs = tmp + ',' + enc_session

    id = cs.split(',')[0]
    enc_s = cs.split(',')[1]

    if ( id != 'guest' and id != 'admin' ):
        print 'invalid id.'
        return

    print 'hello, ' + id + '.'

    session = AESDecrypt(enc_s)

    if ( type(session) == int ):
        if ( session == -1 ):
            print "invalid cipher text. could not process decryption xd"
        else:
            print 'invalid padding(' + str(session) + ') xd'
        return

    elif ( type(session) == str ):
        if  ( session != FindSessionById('admin') ):
            print 'only user "admin" can see flag :('
        else:
            print 'ok. here\'s flag.'
            print ReadFile('flag')
            exit()

#
# #known account
# id: guest
# pw: 714d0ea3d35368817a2656a5884c722e
#
def Login():
    global is_logged_in, enc_session

    if ( is_logged_in == True ):
        print 'you are already logged in.'
        return

    id = raw_input('input id: ')
    pw = raw_input('input pw: ')

    if ( id != 'guest' and id != 'admin' ):
        print 'invalid id.'
        return

    if ( (id == 'guest' and pw != guest_pw) or (id == 'admin' and pw != admin_pw) ):
        print 'pw doesn\'t match.'
        return

    enc_session = StartSession(id)

    is_logged_in = True
    print 'you logged in as "' + id + '".'
    print 'your encrypted session: ' + enc_session

def ChangeSession():
    global enc_session

    if ( is_logged_in == False ):
        print 'login first plz :)'
        return

    enc_session = AESEncrypt(raw_input('input session: '))

def Menu():
    menu = -1

    while ( menu != MENU_QUIT ): 
        print ' << menu >>'
        print '1. see flag'
        print '2. login'
        print '3. change session'
        print '4. quit'

        menu = InputNumber()
        if ( menu == MENU_SEE_FLAG ):
            SeeFlag()
        elif ( menu == MENU_LOGIN ):
            Login()
        elif ( menu == MENU_CHANGE_SESSION):
            ChangeSession()
        elif ( menu == MENU_QUIT ):
            print 'quitting...'
            break
        else:
            print 'invalid menu.'

is_logged_in = False
enc_session = ''
guest_pw = ReadFile(ABS_PATH + 'password/guest')
admin_pw = ReadFile(ABS_PATH + 'password/admin')

if ( __name__ == '__main__' ):
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)
    sys.stderr = os.fdopen(sys.stderr.fileno(), 'w', 0)
    Menu()

