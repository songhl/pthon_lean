#!/usr/bin/env python
#coding:utf-8
#time: 2016/5/3 9:11
__author__ = 'songhailong' 
import  time
def countdown(n):
    while n >0:
        print('T-minus',n)
        n -= 1
        time.sleep(5)
#create and launch a thread
from threading import Thread
t=Thread(target=countdown,args=(10,))
# if t.is_alive():
#     print("still running")
# else:
#     print("Completed")
t.start()
import commands