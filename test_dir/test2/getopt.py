#!/usr/bin/env python
#coding:utf-8
#time: 2015/12/22 10:43
__author__ = 'songhailong' 
import getopt
import sys
opts, args = getopt.getopt(sys.argv[1:],'a:b:d')
opts = dict(opts)
print opts.has