#!/usr/bin/env python
#coding:utf-8
#time: 2016/5/4 0:43
__author__ = 'songhailong' 
import time
import multiprocessing
from threading import Thread
class CountdownThread(Thread):
    def __init__(self, n):
        #super().__init__()
        self.n = 0
    def run(self):
        while self.n > 0:

            print('T-minus', self.n)
            self.n -= 1
            time.sleep(5)

#c = CountdownThread(5)
#c.start()
c=CountdownThread(5)
#c.start()
def test(n):
    l=[1,2,3,4,5,6,7,8]
    for i in range(n):
        print(l[i])
d=test(5)
p=multiprocessing.Process(target=d)
p.start()