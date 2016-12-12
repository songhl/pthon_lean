#!/usr/bin/env python
#coding:utf-8
#time: 2016/1/14 17:17

__author__ = 'songhailong' 
names=['anne','beth','george','damon']
ages=[12,45,32,102]
for i in range(len(names)):
    print(names[i],'is',ages[i],'years old')
print("第二种迭代方法(zip)")
for name,age in zip(names,ages):
    print(name,'is',age,'years old')

from math import sqrt
for n in range(99,0,-1):
    root=sqrt(n)
    if root == int(root):
        print n
        break
while True:
    word=raw_input("please enter a word:")
    if  word=="hailong":
        break
    print("the word was "+word)