#!/usr/bin/env python
#coding:utf-8
#time: 2017/1/7 21:20
import urllib
import urllib2
import cookielib
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
refere = 'http://zabbixm.mysql.jddb.com/index.php'
headers = {'User-Agent' : user_agent,'Referer' : refere }
# url2 = 'http://zabbixm.mysql.jddb.com/dashboard.php'
url = 'http://zabbixm.mysql.jddb.com/index.php'
values = {'name' : 'songhailong','password' : 'songhailong', 'autologin': '1','enter' : 'Sign+in'}
# cookie
cj = cookielib.LWPCookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
urllib2.install_opener(opener)
#
data = urllib.urlencode(values)
request = urllib2.Request(url,data,headers=headers)
response = urllib2.urlopen(request)

# opener = urllib2.build_opener(handler)
# response = opener.open(request)
the_page = response.read()
print(the_page)
# print(cookie,"--------",response.read())