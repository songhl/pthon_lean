#!/usr/bin/env python
#coding:utf-8
#time: 2016/1/21 11:30
__author__ = 'songhailong' 

def fibs(num):
    result = [0,1]
    for i in range(num-2):
        result.append(result[-2]+result[-1])
    return  result

print(fibs(10))
def test():
    print('This is priinted')
    return
    print('This is not')

x=test()
print(str(x)+"aa")
print("==================")
n="songhailong"
print(n)
def value():
    n="song"
    print(n)
value()
print(n)