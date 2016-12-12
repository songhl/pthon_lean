#!/usr/bin/env python
#coding:utf-8
#time: 2016/6/6 16:55
__author__ = 'songhailong'
import re
f=open('ip','r')
for resa in f:
    res=resa.strip()
    print(res)
    iplist=[]
    num=0
    # for z_ip in gr:
    #     print z_ip