#!/usr/bin/env python
#coding:utf-8
__author__ = 'songhailong'
import MySQLdb
def test(sql):
    try:
        conn = MySQLdb.connect(charset='utf8',host='192.168.1.10',port = 3358,user =  'root',passwd =  'hailong',db='noya')
        #cursor = conn.cursor() #以元组返回
        cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor) #以字典形式返回
        cursor.execute(sql)
        alldata = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        return alldata
    except Exception,e:
        print e
        return '0'
sql="select noya_dns,old_ip from noya.sys limit 3;"
n=1
aa=test(sql)
#print aa
for i in aa:
    #print ("%s:%s" %(n,i[0]))
    print i
    print("id:%s DNS:%s IP:%s" % (n,i['noya_dns'],i['old_ip']))
    n+=1
