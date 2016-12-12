#!/usr/bin/env python
#coding:utf-8
#time: 2016/1/22 15:13
__author__ = 'songhailong' 
def story(**kwds):
    return 'Once upon a time,there was a '\
            '%(job)s cakked %(name)s.' % kwds
def power(x,y,*others):
    if others:
        print('Received redundant parameters:',others)
    return pow(x,y)
def interval(start,stop=None,step=1):
    'Imitates range() for step > 0'
    if stop is None:
        start,stop=0,start
    result=[]
    i=start
    True 
    while i < stop:
        result.append(i)
        i+=step
    return  result
print(story(job='king',name='Gumby'))
print(story(name='Sir Robin',job='brave knight'))
params={'job':'language','name':'Python'}
print(story(**params))
del params['job']
print(story(job='stroke of genius',**params))

print(power(2,3))
print(power(x=3,y=2))

params=(5,)*2
print(power(*params))
print(power(3,3,'hello world'))

print(interval(10))
print(interval(1,5))
