#!/usr/bin/env python
#coding:utf-8
#time: 2016/5/3 23:56
__author__ = 'songhailong' 
class IOTask:
    def terminate(self):
        self._running=False
    def run(self,sock):
        sock.settimeout(5)
        while self._running:
            try:
                data=sock.recv(8192)
                break
            except sock.timeout:
                continue
        return