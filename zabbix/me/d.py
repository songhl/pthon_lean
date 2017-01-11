#!/usr/bin/env python
#coding:utf-8
#time: 2017/1/11 15:22
#http://www.cnblogs.com/dreamer-fish/p/5484767.html
import urllib,urllib2,cookielib
login_url='http://zabbixm.mysql.jddb.com/index.php'
login_data=urllib.urlencode({
    "name": "songhailong",
    "password": "songhailong",
    "autologin": 1,
    "enter":"Sign+in"
})
refere = 'http://zabbixm.mysql.jddb.com/index.php'
headers={
    refere:refere,
    'Host':'zabbixm.mysql.jddb.com',
    'User-Agent':'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)'
}
#
cj= cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
urllib2.install_opener(opener)
#
req=urllib2.Request(login_url,login_data,headers)
response=urllib2.urlopen(req)
print(response.read())