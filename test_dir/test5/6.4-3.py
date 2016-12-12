#!/usr/bin/env python
#coding:utf-8
#time: 2016/1/22 11:38
__author__ = 'songhailong' 

def hello1(greeting,name):
    print('%s, %s!' % (greeting,name))
def hello2(name,greeting):
    print('%s, %s!' % (greeting,name))

hello1('hello','world')
hello2('Hello','World')
hello1(greeting='world',name='hello')

def print_params(*params):
    print params

print_params(1,2,3)
print_params('song','hai','long')
#显示为元组
def print_params2(title,*params):
    print(title)
    print(params)
print_params2('song','hailong','hello')
#显示为字典
def print_params3(**params):
    print(params)
print_params3(x=1,y=2,z=3)