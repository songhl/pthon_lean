#!/usr/bin/env python
#coding:utf-8
#time: 2016/5/17 16:25
__author__ = 'songhailong' 
import  pymysql
def test(sql):
    try:
        conn=pymysql.connect(host='192.168.1.10',user='root',passwd='hailong',db='mysql',port=3306,charset='utf8')
        #cur=conn.cursor()
        cur=conn.cursor()
        cur.execute(sql)
        # data=cur.fetchall()
        # print(data)
        for r in cur:
            print r
        cur.close()
        conn.close()
    except exception,e:
        print e
if __name__ == '__main__':
    sql='select user,host,password from user'
    u=test(sql)
    print u