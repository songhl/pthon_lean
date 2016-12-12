#!/usr/bin/env python
#coding:utf-8
#time: 2015/12/25 15:47
__author__ = 'songhailong' 
import datetime
import sys
import time
spring=datetime.datetime(2016,2,8,0,0,0)    #春节日期
while  True:
        pass
        today=datetime.datetime.now()        #今天是几月几号
        day=(spring-today).days              #得到还有几天
        second=(spring-today).seconds     #得到还有几秒
        sec=second%60                   #根据秒数得到还有几秒
        minute=second/60%60             #根据秒得到分钟数
        hour=second/60/60        #根据秒数得到小时
        if hour>24:
                hour=hour-24    #如果超过24小时，就要算超过1天，所以要减去24
        sys.stdout.write( "离今年春节还有"+str(day)+"天"+str(hour)+"小时"+str(minute)+"分钟"+str(sec)+"秒"+'\r')
#       sys.stdout.write( "离今年春节还有 %d 天 %d 小时 %d 分钟 %d 秒 \r "  %(day,hour,minute,sec) )
        sys.stdout.flush()
        time.sleep(1)