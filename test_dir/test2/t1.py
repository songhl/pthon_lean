#!/usr/bin/env python
#coding:utf-8
__author__ = 'songhailong'

import math
import string
print('%010.2f' % math.pi)  # 用另来填充空格
print('%-10.2f' % math.pi)
#
print(string.digits)
print(string.printable)
print(string.punctuation)
print(string.letters)
print(string.uppercase)
#3.4.1 and2
title='with a moo-moo here, and a moo-moo there'
print(title.find('with'))
a="this is python"
print (a.find("python,is"))
print("python,is" in a)   #判断Trun 或False