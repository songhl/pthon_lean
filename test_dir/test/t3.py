#!/usr/bin/env python
#coding:utf-8
__author__ = 'songhailong'

user_name=12121
print("your are name "+`user_name`)
#等价于下面语句
print("your are name "+repr(user_name))
#########################################
print("your are name "+str(user_name))

print(type(repr(user_name)))