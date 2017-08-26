import angr
import simuvex
import claripy
import urllib
import urllib2
PHPSESSID = ""
def solver(name,find):
    p = angr.Project(name,load_options={'auto_load_libs': False})

    ans = claripy.BVS('ans',100*8)
    init = p.factory.entry_state(args=['./prob',ans])
    init.options.remove(simuvex.o.LAZY_SOLVES)

    pg = p.factory.path_group(init)
    ex = pg.explore(find=find)

    s = pg.found[0].state
    return s.se.any_str(ans)

def getsessid():
    url = "http://110.10.212.131:8777/"
    user_agent = "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)"
    req = urllib2.Request(url)
    req.add_header("User-agent", user_agent)
    response = urllib2.urlopen(req)
    header = response.info().headers
    SESSID = header[header.find('SESSID=')+7:]
    SESSID = SESSID[:SESSID.find('\n')]
    print SESSID
    return SESSID

def sendkey(i,key):
    url = "http://110.10.212.131:8777/auth.php"
    user_agent = "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)"
    data = {'prob':str(i), 'key':key}
    data = urllib.urlencode(data)
    req = urllib2.Request(url,data)
    req.add_header("User-agent", user_agent)
    req.add_header("Cookie", "PHPSESSID="+PHPSESSID)
    response = urllib2.urlopen(req)
    print response.read()
    
def main():
    PHPSESSID = getsessid()
    seeker = "\x55\x48\x89\xE5\x48\x83\xEC\x10\x89\x7D\xFC\x48\x89\x75\xF0\x83"
    for i in range(1,102):
        fname = "prob"+str(i)
        f = open(fname,"rb")
        find = f.read().find(seeker)+0x400050
        f.close()
        KEY = solver(fname,find)
        KEY = KEY.replace("\x00",'')
        print str(i)+" "+KEY
        sendkey(i,KEY)
    url = "http://110.10.212.131:8777/"
    user_agent = "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)"
    req = urllib2.Request(url)
    req.add_header("User-agent", user_agent)
    req.add_header("Cookie", "PHPSESSID="+PHPSESSID)
    response = urllib2.urlopen(req)
    print response.read()
if __name__ == "__main__":
    main()
