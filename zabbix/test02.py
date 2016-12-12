#!/usr/bin/env python
#coding:utf-8
#time: 2016/11/28 17:05
__author__ = 'songhailong' 
#!/usr/bin/python
#coding:utf-8
import json
import urllib2
from urllib2 import URLError
class ZabbixTools:
    def __init__(self,address,username,password):

        self.address = 'http://zabbixm.mysql.jddb.com'
        self.username = 'songhailong'
        self.password = 'songhailong'

        self.url = '%s/api_jsonrpc.php' % self.address
        self.header = {"Content-Type":"application/json"}



    def user_login(self):
        data = json.dumps({
                           "jsonrpc": "2.0",
                           "method": "user.login",
                           "params": {
                                      "user": self.username,
                                      "password": self.password
                                      },
                           "id": 0
                           })

        request = urllib2.Request(self.url, data)
        for key in self.header:
            request.add_header(key, self.header[key])

        try:
            result = urllib2.urlopen(request)
        except URLError as e:
            print "Auth Failed, please Check your name and password:", e.code
        else:
            response = json.loads(result.read())
            result.close()
            print response['result']
            self.authID = response['result']
            return self.authID

    def trigger_get(self):
        data = json.dumps({
                           "jsonrpc":"2.0",
                           "method":"trigger.get",
                           "params": {
                                      "output": [
                                                "triggerid",
                                                "description",
                                                "priority"
                                                ],
                                      "filter": {
                                                 "value": 1
                                                 },
                                      "expandData":"hostname",
                                      "sortfield": "priority",
                                      "sortorder": "DESC"
                                    },
                           "auth": self.user_login(),
                           "id":1
        })

        request = urllib2.Request(self.url, data)
        for key in self.header:
            request.add_header(key, self.header[key])

        try:
            result = urllib2.urlopen(request)
        except URLError as e:
            print "Error as ", e
        else:
            response = json.loads(result.read())
            result.close()

ZabbixTools.trigger_get()