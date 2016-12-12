#!/usr/bin/env python
#coding:utf-8
__author__ = 'songhailong'

import MySQLdb
# conn=MySQLdb.connect(charset='utf8',host='192.168.1.82',port = 3306,user =  'root',passwd =  '',db='mysql')
# cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
# sql='show processlist'
# cursor.execute(sql)
# alldata = cursor.fetchall()
# conn.commit()
# cursor.close()
# conn.close()
def adm(sql):
    try:
        conn = MySQLdb.connect(charset='utf8',host='192.168.1.82',port = 3306,user =  'root',passwd =  '',db='mysql')
        cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        cursor.execute(sql)
        alldata = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        return alldata
    except Exception,e:
        print e
        return '0'
info=adm('select * from information_schema.processlist')
num=1
filename='processlist.txt'
file=open(filename,'w')
for i in info:
    f="******************** %s. row *********************\n" % num
    file.write(f)
    num+=1
    for k,v in i.items():
        f="%s : %s\n" % (k,v)
        file.write(f)
file.close()