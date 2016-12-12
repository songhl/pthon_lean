#!/usr/bin/env python
#coding:utf-8
__author__ = 'songhailong'


a = 'update mysql set user="root" where user="3000" ;'
b = a.split(" ")
print(b)

update=b.index("update")
se=b.index("set")
print(update,se)
table_name=b[b.index("update")+1]
print (table_name)
sql1=b[update:se]
print(sql1)