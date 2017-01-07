#!/usr/bin/env python
#coding:utf-8
#time: 2016/11/28 16:38
__author__ = 'songhailong' 
from zabbix_api import ZabbixApi
api_info = {
    'url':  'http://zabbixm.mysql.jddb.com/api_jsonrpc.php',
    'user': 'songhailong',
    'password': 'songhailong'
}
zbxapi = ZabbixApi(api_info)
zbxapi.login()
# a=zbxapi.get_shl('172.20.129.117')
a=zbxapi.get_hostname_shl('172.20.129.117')
print(a)