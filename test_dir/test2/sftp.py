#!/usr/bin/env python
#coding:utf-8
#time: 2016/2/23 18:34
__author__ = 'songhailong' 
import paramiko
try:
    t= paramiko.Transport(("192.168.1.11",22))
    t.connect(username="root",password="hailong")
    sftp=paramiko.SFTPClient.from_transport(t)
    remotepath='/tmp/123.txt'
    localpath='E:\out_data\user.TXT'
    sftp.put(localpath,remotepath)
    sftp.get(re)
    t.close()
except Exception,e:
    print e
    #return 0

