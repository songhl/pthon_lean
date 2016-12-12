#!/usr/bin/env python
#coding:utf-8
__author__ = 'songhailong'
a="192.168.1.20"
b=["hello","song"]
print(list(a))
print(list(b))
#print(list(b))
c=list(a)
c[1]="long"
print(c)
del c[1]
print(c)

d=[1,2,3,4,5,6,7]
d.append(d.pop())
print d



k=["we","are","the","k","who","the"]
k.remove('the')
print(k)