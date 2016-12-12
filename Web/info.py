#!/usr/bin/env python
#coding:utf-8
#time: 2016/4/28 10:53
__author__ = 'songhailong'
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
f=open("info","r")
dic=dict()
for i in f:
    line=i.strip().split("=")
    #print i
    if len(line)>1:
        dic[line[0]]=line[1]
    else:
        dic[line[0]]=''
f.close()
print(dic)