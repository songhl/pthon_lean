#!/usr/bin/env python
#coding:utf-8
#time: 2016/8/4 9:42
__author__ = 'songhailong'
import re
from fabric.colors import *
f=open('zabbix','r')
iplist=[]
for info in f:
    if re.search(r'^(10|172)\.',info):
        ip=info.split()[0].strip()
        iplist.append(ip)
        print(ip)
ips=" ".join(iplist)
print ips+"\n"