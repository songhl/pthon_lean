#!/usr/bin/env python
#coding:utf-8
__author__ = 'songhailong'

from string import maketrans   # 引用 maketrans 函数。

intab = "aeiou"
outtab = "12345"
trantab = maketrans(intab, outtab)

str = "this is string example....wow!!!";
print (str.translate(trantab));