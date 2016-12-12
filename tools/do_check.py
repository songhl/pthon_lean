#!/usr/bin/env python
#coding:utf-8
#time: 2016/3/10 10:56
__author__ = 'songhailong'
import MySQLdb
import json
def jd_sys(sql):
    try:
        conn = MySQLdb.connect(charset='utf8',host='192.168.137.100',port = 3358,user =  'songhailong',passwd =  'songhailong',db='jdmysqlmgrsys')
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
def jd_test(sql):
    try:
        conn = MySQLdb.connect(charset='utf8',host='192.168.1.11',port = 3306,user =  'root',passwd =  'hailong',db='jmms')
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
def jd_test2(sql):
    try:
        conn = MySQLdb.connect(charset='utf8',host='192.168.1.11',port = 3306,user =  'root',passwd =  'hailong',db='jdmysqlmgrsys')
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
def jmms(sql):
    try:
        conn = MySQLdb.connect(charset='utf8',host='172.22.220.73',port = 3358,user =  'songhailong',passwd =  'songhailong',db='jmms')
        cursor = conn.cursor()
        cursor.execute(sql)
        alldata = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        return alldata
    except Exception,e:
        print e
        return '0'
if __name__ == '__main__':
    sql="select id from t_cluster limit 5"
    f=jd_test(sql)
    print(f)
    for c_id in f:
        ip_sql='select ip from t_machine where status=1 and cluster_id='+str(c_id['id'])+' and ip not in(select ip from backup_blacklist)'
        ip_num=jd_test(ip_sql)
        mun=0
        iplist=[]
        if len(ip_num)>0:
            for ip_n in ip_num: #查询一套集群中iplist
                sql_c='select b.backup_ip from mgr_backup b,mgr_machine m where m.id=b.machine_id and date_format(b.endtime,"%Y%m%d")=date_format(NOW(),"%Y%m%d") and m.ip="'+str(ip_n['ip'])+'"'
                ss=jd_test2(sql_c) #检查每一个ip是否备份数据
                if len(ss)>0:
                    mun=mun+1
                    iplist.append(str(ip_n['ip']))
            if mun==0:
                print('id:%s clustrt:%s: not backup' % (c_id,ip_num))
            elif mun==1:
                #print('cluster:%s backup success' % str(ip_num))
                pass
            elif mun>=2:
                print('cluster:%s Repeat backup,iplist:%s' % (ip_num,iplist))




