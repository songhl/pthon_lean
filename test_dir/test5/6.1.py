#!/usr/bin/env python
#coding:utf-8
#time: 2016/1/18 9:41
__author__ = 'songhailong' 
fibs=[0,1]
for i in range(8):
    fibs.append(fibs[-2]+fibs[-1])
    print(fibs)
print(fibs)