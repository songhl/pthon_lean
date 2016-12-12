#!/usr/bin/env python
#coding:utf-8
__author__ = 'songhailong'

import _mysql_connector
# 创建连接
config = {
          'user':'root',
          'password':'hailong',
          'host':'192.168.1.10',
          'port':3358,
          'database':'mysql'}
print config
#conn = mysql.connector.connect(**config)
# 创建游标
#cur = conn.cursor()
# 执行查询SQL
#sql = "SELECT user,host,password from mysql.user"
#cur.execute(sql)
# 获取查询结果
#result_set = cur.fetchall()
#if result_set:
#    for row in result_set:
#        print "%s, %s, %s" % (row[0],row[1],row[2])
# 关闭游标和连接
#cur.close()
#conn.close()