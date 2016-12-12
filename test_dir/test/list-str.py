#!/usr/bin/env python
#coding:utf-8
#time: 2016/1/6 18:05
__author__ = 'songhailong' 
# s=''
# l=[1,2,3,4]
# n=0
# while n < len(l):
#     s += str(l[n])+","
#     n += 1
# #print(s)
#
# #print ','.join(l)
#
# m=open("iplist","r")
# #txt=m.read()
# #print(txt.strip())
# n=1
# for i in m:
#     ip=i.strip()
#     print(ip)
#     ss=ss+str(ip)
#     print ss


from selenium import webdriver
driver = webdriver.Firefox()

driver.maximize_window()

driver.get('http://www.baidu.com')