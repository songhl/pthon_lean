#!/usr/bin/env python
#coding:utf-8
#time: 2016/1/5 11:34
__author__ = 'songhailong'
import paramiko
username="root"
passwd="hailong"
def ssh(ip,user,password,cmd):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip,22,user,password)
    stdin,stdout,stderr = ssh.exec_command(cmd)
    #print(stdout.readlines())
    print(stdout.read())
    ssh.close()
def exec_com(host,comnd):
    try:
        s=paramiko.SSHClient()
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        s.connect(hostname=host,port=22,username=username,password=passwd)
        stdin,stdout,stderr=s.exec_command(comnd)
        result = stdout.readlines()
        s.close()
    except Exception,e:
        print(e)
        return 0
if __name__ == '__main__':
    #a=ssh('192.168.1.11',"root","hailong","df -Th")
    print exec_com('192.168.1.11',"df -Th")
