#!/usr/bin/env python
#coding:utf-8
#time: 2016/3/28 17:57
__author__ = 'songhailong'
import threading
import time
import random
lock = threading.Lock()  # 生成一个锁对象，用来作互斥操作


class MyThread(threading.Thread):

    def __init__(self, func, args, name='no_name'):
        u'''
        func:传入的函数名称;
        args是func的参数,注意仅一个参数时,使用(args,)的形式
        '''
        threading.Thread.__init__(self)
        self.name = name
        self.func = func
        self.args = args
        self.res = None

    def run(self):
        self.res = apply(self.func, self.args)
        return self.res


def fun(name):
    sleep_sec = 10 * random.random()
    time.sleep(sleep_sec)
    lock.acquire()
    print('i am thread %s,has slept %f seconds.' % (name, sleep_sec))
    lock.release()

list_t = []
for i in range(5):
    name = str(i)
    t = MyThread(func=fun, args=(name,))
    t.setDaemon(True)  # 设置线程为daemon，意义是：主线程会把daemon线程结束后再退出。
    t.start()  # 线程开始运行
    list_t.append(t)
for t in list_t:
    t.join()  # 主线程阻塞等待list_t中所有线程结束后，继续运行
print 'All done'