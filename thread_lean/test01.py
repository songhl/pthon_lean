#!/usr/bin/env python
#coding:utf-8
#time: 2016/11/28 15:55
__author__ = 'songhailong' 

from multiprocessing import Process,Manager
# def f(name):
# 	print "hello",name
# if __name__ == '__main__':
# 	a=['abc','aa','hrgrae','greagh']
# 	p = Process(target = f, args = (a,))
# 	p.start()
# 	p.join()
manger = Manager()
d=manger.list(range(10))
print(d)
