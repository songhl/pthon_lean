#!/usr/bin/env python
#coding:utf-8
#time: 2017/1/10 15:40
import HTMLParser
import urlparse
import urllib
import urllib2
import cookielib
import string
import re

#登录的主页面
hosturl = 'http://172.28.76.123/index.php' #自己填写
#post数据接收和处理的页面（我们要向这个页面发送我们构造的Post数据）
posturl = 'http://172.28.76.123/dashboard.php' #从数据包中分析出，处理post请求的url

#设置一个cookie处理器，它负责从服务器下载cookie到本地，并且在发送请求时带上本地的cookie
cj = cookielib.LWPCookieJar()
cookie_support = urllib2.HTTPCookieProcessor(cj)
opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
urllib2.install_opener(opener)

#打开登录主页面（他的目的是从页面下载cookie，这样我们在再送post数据时就有cookie了，否则发送不成功）
h = urllib2.urlopen(hosturl)

#构造header，一般header至少要包含一下两项。这两项是从抓到的包里分析得出的。
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1',
           'Referer' : 'www.jd.com'}
#构造Post数据，他也是从抓大的包里分析得出的。
postData = { 'user' : 'songhailong', #你的用户名
            'pass' : 'songhailong', #你的密码，密码可能是明文传输也可能是密文，如果是密文需要调用相应的加密算法加密
             'autologin' : '1',
             'enter':'Sign+in'
            # 'rmbr' : 'true',   #特有数据，不同网站可能不同
            # 'tmp' : '0.7306424454308195'  #特有数据，不同网站可能不同

            }

#需要给Post数据编码
postData = urllib.urlencode(postData)

#通过urllib2提供的request方法来向指定Url发送我们构造的数据，并完成登录过程
request = urllib2.Request(posturl, postData, headers)
# print request
response = urllib2.urlopen(request)
text = response.read()
print text