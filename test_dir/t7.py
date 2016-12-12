#!/usr/bin/env python
#coding:utf-8
#time: 2016/10/8 9:11
__author__ = 'songhailong' 
# import sqlparse
# sql='''select a.id,b.cid,c.n    from t1 a, t2 c where a.id=c.id'''
# a=sqlparse.sql.Statement(sql)
# print(a)


import datetime
yesterday=datetime.datetime.now() - datetime.timedelta(days=1)
three_day_ago=datetime.datetime.now() - datetime.timedelta(days=2)
print(yesterday,three_day_ago)
yesterday,three_day_ago=yesterday.strftime("%Y-%m-%d"),three_day_ago.strftime("%Y-%m-%d")
print(yesterday,three_day_ago)



day=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print day