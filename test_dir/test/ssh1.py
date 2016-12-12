#!/usr/bin/env python
#coding:utf-8
#time: 2015/12/24 16:55
import paramiko
import threading
def ssh(ip,cmd):
    try:
        ssh=paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip,22,"root","hailong",timeout=5)
        for m in cmd:
            stdin, stdout, stderr = ssh.exec_command(m)
            stdin.write("Y")
            out = stdout,readlines()
            for o in out:
                print o
        print('%s\tOK\n'%(ip))
        ssh.close()
    except:
        print('%s\tError\n'%(ip))
if __name__=='__main__':
    ssh('192.168.1.11',"df -h")