#!/usr/bin/env python
#coding:utf-8
#time: 2016/11/22 16:40
__author__ = 'songhailong' 
import datetime
print("打印现在时间")
print(datetime.datetime.now())
print("以string形式打印")
print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
print("打印时间date形式")
print(datetime.datetime.now().date())
print("获取当前时间")
print(datetime.date.today())

print("获取明天/前N天")
print(datetime.date.today() + datetime.timedelta(days=1))

# 3天前
print(datetime.datetime.now() - datetime.timedelta(days=3))
# 获取当天开始和结束时间(00:00:00 23:59:59)
print(datetime.datetime.combine(datetime.date.today(), datetime.time.min))
print(datetime.datetime.combine(datetime.date.today(), datetime.time.max).strftime("%Y-%m-%d %H:%M:%S"))

# 获取两个datetime的时间差
print((datetime.datetime(2015,1,13,12,0,0) - datetime.datetime.now()).total_seconds())

# 获取本周/本月/上月最后一天
# 本周
today = datetime.date.today()
sunday = today + datetime.timedelta(6 - today.weekday())
print(sunday)
# 本月
import calendar
today = datetime.date.today()
_, last_day_num = calendar.monthrange(today.year, today.month)
last_day = datetime.date(today.year, today.month, last_day_num)
print(last_day)
# 获取上个月的最后一天(可能跨年)
today = datetime.date.today()
first = datetime.date(day=1, month=today.month, year=today.year)
lastMonth = first - datetime.timedelta(days=1)
print(lastMonth)


# 关系转换例子
# datetime -> string
print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
print "string -> datetime"
print(datetime.datetime.strptime("2014-12-31 18:20:10", "%Y-%m-%d %H:%M:%S"))