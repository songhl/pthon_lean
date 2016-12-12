#!/usr/bin/env python
#coding:utf-8
#time: 2016/1/14 17:09
__author__ = 'songhailong'
d={'x':1,'y':1,'z':3}
print(d)
print("第一种遍历方法")
for key in d:
    print(key,'corresponds to ',d[key])
print("第二种遍历方法")
for key,value in d.items():
    print(key,'corresponds to ',value)