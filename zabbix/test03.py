#!/usr/bin/env python
#coding:utf-8
#time: 2016/11/28 18:12
__author__ = 'songhailong' 
import json,urllib2,random,linecache,MySQLdb
url = "http://zabbixm.mysql.jddb.com/api_jsonrpc.php"
user = "songhailong"
pwd = "songhailong"
header = {"Content-Type": "application/json-rpc"}
def user_login():
	data = json.dumps(
		{
		"jsonrpc": "2.0",
		"method": "user.login",
		"params": {
		"user": user,
		"password": pwd
		},
		"id": 0
		})
	request = urllib2.Request(url,data)
	for key in header:
		request.add_header(key,header[key])
	try:
		result = urllib2.urlopen(request)
	except URLError as e:
		print "Auth Failed, Please Check Your Name And Password:",e.code
	response = json.loads(result.read())
	result.close()
	authID = response['result']
	return authID
user_login()
def get_data(self,data,hostip=""):
    request = urllib2.Request(self.url,data)
    for key in self.header:
        request.add_header(key,self.header[key])
    try:
        result = urllib2.urlopen(request)
    except URLError as e:
        if hasattr(e, 'reason'):
            print 'We failed to reach a server.'
            print 'Reason: ', e.reason
        elif hasattr(e, 'code'):
            print 'The server could not fulfill the request.'
            print 'Error code: ', e.code
        return 0
    else:
        response = json.loads(result.read())
        result.close()
        return response
def get_tri():
	data = json.dumps({
		"jsonrpc": "2.0",
		"method": "trigger.get",
		"params": {
		"output": "extend",
		"selectLastEvent": "extend"
		},
		"auth": user_login,
		"id" : 1
		})
    print data
	# res = get_data(data)
	# print res

get_tri()