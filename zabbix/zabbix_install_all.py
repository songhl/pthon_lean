#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os,sys,time,MySQLdb,threading,datetime
import paramiko,socket
import add_host_to_zabbix

def to_log(task,text):
    day = time.strftime("%Y-%m-%d")
    if task == 1:
        logfile = "/export/wangwei/zabbix/log/zabbix_success_%s.log" % day
    else:
        logfile = "/export/wangwei/zabbix/log/zabbix_error_%s.log" % day
    now = time.strftime("%Y-%m-%d %H:%M:%S")
    tt = str(now) + "\t" + str(text) + "\n"
    f = open(logfile,'a+')
    f.write(tt)
    f.close()

def get_port(host):
    socket.setdefaulttimeout(30)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, 10050))
        s.close()
        return 1
    except socket.error, msg:
        return 0

def exec_command(host,hostname,proxyip,mysql_port):
    username = 'root'
#    passwd = 'Na4hycxdsk]hu0vkgnzig$x' #HK
#    passwd = 'byfLMurtD8E7O4xNmdznCsoYS3UJIq' #yonghu
#    passwd = 'huvEm$e5gv}Fihgdp*ifnqwet7' # Old password
    passwd = 'vef9oX$irzuxrfq_Wtkbqtabsj9djy'
    port = 22
    try:
        s=paramiko.SSHClient()
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        s.connect(hostname = host,port=port,username=username, password=passwd)
        comn = 'yum install wget -y && wget http://172.22.184.61/zabbix_install/install_zabbix_agent.sh -O /tmp/install_zabbix_agent.sh && /bin/sh /tmp/install_zabbix_agent.sh %s %s %s && /bin/rm -rf /tmp/install_zabbix_agent.sh' % (hostname,proxyip,mysql_port)
        #print comn
        stdin,stdout,stderr=s.exec_command(comn)
        result = stdout.readlines()
        s.close()
        return result
    except Exception,e:
        print host,e
        return 0

def zabbix_center(center_ip,center_user,center_passwd,sql,port=''):#连接zabbix数据库
    if port == '':
        port = 3358
    else:
        port = int(port)
    try:
        conn = MySQLdb.connect(host = center_ip,port = port,user = center_user,passwd = center_passwd,charset='utf8',connect_timeout=10)
        cursor = conn.cursor()
        cursor.execute(sql)
        alldata = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        return alldata
    except Exception,e:
        print e
        return 0

def check_slave(host,mysql_port):
    flag = '-M-'
    slave_flag = 0
    master_flag = 0

    sql = "SHOW SLAVE STATUS"
    check_slave = zabbix_center(host,'monitor','EhtRreAyVunYKjXQ',sql,mysql_port)
    if check_slave != 0:
        if len(check_slave)>0:
            if check_slave[0].count('Yes') == 2:
                slave_flag = slave_flag + 1
    else:
        flag = 0
        return flag

    sql = "SELECT * FROM information_schema.PROCESSLIST WHERE USER='replicater'"
    check_master = zabbix_center(host,'monitor','EhtRreAyVunYKjXQ',sql,mysql_port)
    if check_master != 0:
        if len(check_master)>0:
            master_flag = master_flag + 1
    else:
        flag = 0
        return flag

    if slave_flag == 1 and master_flag == 1:
        flag = '-MS-'
    elif slave_flag == 0 and (master_flag == 1 or master_flag == 0):
        flag = '-M-'
    elif slave_flag == 1 and master_flag == 0:
        flag = '-S-'
    return flag


def main():
    center_ip = '192.168.137.100'
    center_user = 'hvip'
    center_passwd = 'yvhkfhvk_wubi'
    sql = "select ip,zabbix_name,machine_type from jdmysqlmgrsys.mgr_machine where group_id=1 and monitor=0 and ip not in ('172.27.33.38') order by ip;"
    install_iplist = zabbix_center(center_ip,center_user,center_passwd,sql,3306)
    print install_iplist
    for i in install_iplist:
        mysql_port = 3358
        host = i[0]
        type = int(i[2])
        check_flag = check_slave(host,mysql_port)
        if check_flag == 0:
            text = "%s mysql used for user monitor Can not connet" % host
            print text
            to_log(0,text)
            continue
        db_name = i[1].capitalize().strip()
        group_name = db_name
        numblist = ['0','1','2','3','4','5','6','7','8','9','_']
        for ii in range(len(group_name)):
            if group_name[-1] in numblist:
                group_name = group_name[:-1]
            else:
                break
        if group_name == '':
            group_name = db_name
        db_name = db_name + str(check_flag) + host.split('.')[2]+'.'+host.split('.')[3]
        host_type = '.'.join(host.split('.')[:2])
        if (host_type == '172.16' or host_type == '172.19') and type == 0:
            host_name = "YF"+"-"+db_name
            proxy_ip = 'zbxpyf.mysql.jddb.com'
            proxy_name = 'YF_PROXY'
        elif host_type == '172.22' and type == 0:
            host_name = "HC"+"-"+db_name
            proxy_ip = 'zbxphc.mysql.jddb.com'
            proxy_name = 'HC_PROXY'
        elif host_type == '172.17' and type == 0:
            host_name = "YZH"+"-"+db_name
            proxy_ip = 'zbxpyzh.mysql.jddb.com'
            proxy_name = 'YZH_PROXY'
        elif host_type == '192.168' and type == 0:
            host_name = "B28"+"-"+db_name
            proxy_ip = 'zbxphc.mysql.jddb.com'
            proxy_name = 'HC_PROXY'
        elif host_type == '10.4' and type == 0:
            host_name = "SQ"+"-"+db_name
            proxy_ip = 'zbxphc.mysql.jddb.com'
            proxy_name = 'HC_PROXY'
        elif (host_type == '172.20' or host_type == '172.27') and type == 0:
            host_name = "LF"+"-"+db_name
            proxy_ip = 'zbxplf.mysql.jddb.com'
            proxy_name = 'LF_PROXY'
        elif host_type == '172.26' and type == 0:
            host_name = "HK"+"-"+db_name
            proxy_ip = 'zbxphc.mysql.jddb.com'
            proxy_name = 'HC_PROXY'
        elif type == 1:
            host_name = "Docker"+"-"+db_name
            proxy_ip = 'zbxplf.mysql.jddb.com'
            proxy_name = 'LF_PROXY'
        else:
            text = "%s Not find this host in all room" % host
            print text
            to_log(0,text)
            continue
        print host,host_name,group_name
        #exec_result = 1
        #print host,host_name
        exec_result = exec_command(host,host_name,proxy_ip,mysql_port)
        if exec_result != 0:
            if get_port(host):
                install_result = add_host_to_zabbix.main(host,host_name,group_name,proxy_name,type)
                if install_result == 1:
                    text = "%s install zabbix agent and add to zabbix server Successful" % host
                    update_sql = "update jdmysqlmgrsys.mgr_machine set monitor=1 where ip='%s';" % host
                    res = zabbix_center(center_ip,center_user,center_passwd,update_sql,3306)                       
                    print text
                    to_log(1,text)
                else:
                    text = "%s add to zabbix server failed" % host
                    print text
                    to_log(0,text)
            else:
                text = "%s install zabbix agent Error" % host
                print text
                to_log(0,text)
                continue
        else:
            text = "%s can not connet this host,check it" % host
            print text
            to_log(0,text)
            continue

if __name__ == "__main__":
    main()

