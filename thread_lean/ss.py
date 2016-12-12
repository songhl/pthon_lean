#!/usr/bin/env python
#coding:utf-8
#time: 2016/5/3 23:20
import time
from threading import Thread
__author__ = 'songhailong' 
class CountdownTask:
    def __int__(self):
        self._running = True
    def terminate(self):
        self._running = False
    def run(self,n):
        while n>0:
            print('T-minus',n)
            n-=1
            time.sleep(5)
# c=CountdownTask()
# t=Thread(target=c.run,args=(10,))
# t.start()
# c.terminate()
# t.join()
# c.run(10)

def r(string): return with_color(string, 31) # Red
def g(string): return with_color(string, 32) # Green
def y(string): return with_color(string, 33) # Yellow
def b(string): return with_color(string, 34) # Blue
def m(string): return with_color(string, 35) # Magenta
def c(string): return with_color(string, 36) # Cyan
def w(string): return with_color(string, 37) # White

print w('aaaa')