#!/usr/bin/env python
#coding:utf-8
__author__ = 'songhailong'


months = [
    'January',
    'February',
    'March',
    'April',
    'May',
    'June',
    'July',
    'August',
    'September',
    'October',
    'November',
    'December'
]

month = raw_input('请输入数字:')
index=int(month) - 1

print(months[index])