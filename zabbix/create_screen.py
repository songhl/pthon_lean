#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os,sys,socket
import json,urllib2,random,linecache,MySQLdb
from multiprocessing.dummy import Pool as ThreadPool

class zabbixtools:
    def __init__(self):
        self.url = "http://zabbixm.mysql.jddb.com/api_jsonrpc.php"
        self.header = {"Content-Type": "application/json"}
        self.user = "monitor"
        self.passwd = "monitor"
        self.authID = self.user_login()

    def user_login(self):
        data = json.dumps(
                {
                    "jsonrpc": "2.0",
                    "method": "user.login",
                    "params": {
                        "user": self.user,
                        "password": self.passwd
                        },
                    "id": 0
                    })
        request = urllib2.Request(self.url,data)
        for key in self.header:
            request.add_header(key,self.header[key])
        try:
            result = urllib2.urlopen(request)
        except URLError as e:
            print "Auth Failed, Please Check Your Name And Password:",e.code
        else:
            response = json.loads(result.read())
            result.close()
            authID = response['result']
            return authID

    def get_data(self,data,hostip=""):
        request = urllib2.Request(self.url,data)
        for key in self.header:
            request.add_header(key,self.header[key])
        try:
            result = urllib2.urlopen(request)
        except URLError as e:
            if hasattr(e, 'reason'):
                print 'We failed to reach a server.'
                print 'Reason: ', e.reason
            elif hasattr(e, 'code'):
                print 'The server could not fulfill the request.'
                print 'Error code: ', e.code
            return 0
        else:
            response = json.loads(result.read())
            result.close()
            return response

    def get_hostid(self,hostip):
        data = json.dumps(
                {
                    "jsonrpc": "2.0",
                    "method": "host.get",
                    "params": {
                        "output":["name","status","host","groups"],
                        #"output":"extend",
                        "selectGroups":"extend",
                        "filter": {"ip": [hostip]}
                        },
                    "auth": self.authID,
                    "id": 1
                })
        res = self.get_data(data)['result']
        #print res
        hostid = '0'
        if len(res):
            hostid = res[0]['hostid']
        return hostid

    def get_itemid(self,hostid,key_):
        data = json.dumps(
                {
                    "jsonrpc": "2.0",
                    "method": "item.get",
                    "params": {
                        "output": "extend",
                        "hostids": hostid,
                        "search": {
                            "key_": key_
                            },
                        "sortfield": "name"
                },
                "auth": self.authID,
                "id": 1
                })
        res = self.get_data(data)['result']
        itemid = '0'
        if len(res):
            for i in res:
                if i['key_'] == key_:
                    itemid = i['itemid']
                    break
        return itemid

    def get_templateid(self,templatename):
        data = json.dumps(
                {
                    "jsonrpc": "2.0",
                    "method": "template.get",
                    "params": {
                    "output": "extend",
                    "filter": {
                        "host": [templatename]
                    }
                    },
                "auth": self.authID,
                "id": 1
                })
        res = self.get_data(data)['result']
        templateid = '0'
        if len(res):
            templateid = res[0]['templateid']
        return templateid

    def get_proxyid(self,proxyname):
        data = json.dumps(
                {
                    "jsonrpc": "2.0",
                    "method": "proxy.get",
                    "params": {
                        "output": "extend",
                        "selectInterface": "extend"
                    },
                "auth": self.authID,
                "id": 1
                })
        res = self.get_data(data)['result']
        proxyid = '0'
        if len(res):
            for i in res:
                if i['host'] == proxyname:
                    proxyid = i['proxyid']
                    break
        return proxyid

    def get_group_hosts(self,group_name):
        data = json.dumps(
                {
            "jsonrpc": "2.0",
            "method": "hostgroup.get",
            "params": {
                "output": "extend",
                "selectHosts": "extend",
                "filter": {
                    "name": [group_name]
                }
            },
            "auth": self.authID,
            "id": 1
        })
        res = self.get_data(data)['result']
        group_hostsid = []
        if len(res):
            for host in res[0]['hosts']:
                group_hostsid.append(host['hostid'])
            return group_hostsid
        else:
            return '0'

    def get_groupid(self,group_name):
        data = json.dumps(
                {
                "jsonrpc": "2.0",
                "method": "hostgroup.get",
                "params": {
                    "output": "extend", 
                    "filter": {
                        "name": [group_name]
                    }
                },
                "auth": self.authID,
                "id": 1
            })
        res = self.get_data(data)['result']
        if len(res):
            group_id = res[0]['groupid']
            return group_id
        else:
            return '0'

    def add_group(self,group_name):
        data = json.dumps(
                {
                "jsonrpc": "2.0",
                "method": "hostgroup.create",
                "params": {
                    "name": group_name
                },
                "auth": self.authID,
                "id": 1
            })
        res = self.get_data(data)#['result']
        group_id = '0'
        if res.has_key('error'):
            print res['error']['data']
        else:
            if len(res['result']):
                group_id = res['result']['groupids'][0]
        return '0'

    def add_host(self,hostname,hostip,group_name,proxyname,templates):
        groupid = self.get_groupid(group_name)
        if groupid == '0':
            groupid = self.add_group(group_name)
        proxy_hostid = self.get_proxyid(proxyname)
        if proxy_hostid == '0':
            print hostip,"Can not find this proxy:%s" % proxyname
            proxy_hostid = ""
        host_template = []
        for temp in templates.split(','):
            templateid = self.get_templateid(temp)
            temp_dic = {}
            if templateid != '0':
                temp_dic['templateid'] = templateid
                host_template.append(temp_dic)
            else:
                print hostip,"Can not find this template"
        if (len(host_template) > 0) and (proxy_hostid != '0'):
            if proxy_hostid:
                data = json.dumps(
                    {
                    "jsonrpc": "2.0",
                    "method": "host.create",
                    "params": {
                    "host": hostname,
                    "interfaces": [{"type": 1,"main": 1,"useip": 1,"ip": hostip,"dns": "","port": "10050"}],
                    "groups": [{"groupid": groupid}],
                    "templates": host_template,
                    "proxy_hostid": proxy_hostid,
                    },
                    "auth": self.authID,
                    "id": 1
                    })
            else:
                data = json.dumps(
                    {
                    "jsonrpc": "2.0",
                    "method": "host.create",
                    "params": {
                    "host": hostname,
                    "interfaces": [{"type": 1,"main": 1,"useip": 1,"ip": hostip,"dns": "","port": "10050"}],
                    "groups": [{"groupid": groupid}],
                    "templates": host_template,
                    },
                    "auth": self.authID,
                    "id": 1
                    })
            res = self.get_data(data)
            if res.has_key('error'):
                print hostip,res['error']['data']
            else:
                print "Add host success,hostid is %s" % res['result']['hostids'][0]

    def getdel_screen(self,screen_name):
        data = json.dumps(
                {
            "jsonrpc": "2.0",
            "method": "screen.get",
            "params": {
                "output": "extend",
                "selectScreenItems": "extend",
                "filter": {
                    "name": [screen_name]
                }
            },
            "auth": self.authID,
            "id": 1
        })
        res = self.get_data(data)
        if res.has_key('error'):
            print res['error']['data']
            return '0'
        elif len(res['result']) ==0:
            print "Cannot find this screen %s" % screen_name
            return '0'
        else:
            screenid = res['result']
            return screenid[0]['screenid']

    def getdel_graph(self,host):
        hostid = self.get_hostid(host)
        if hostid != '0':
            data = json.dumps(
            {
            "jsonrpc": "2.0",
            "method": "graph.get",
            "params": {
                "output": "extend",
                "hostids": hostid,
                "sortfield": "name"
            },
            "auth": self.authID,
            "id": 1
            })
            res = self.get_data(data)
            if res.has_key('error'):
                print res['error']['data']
            else:
                graph = {}
                for key in res['result']:
                    graph[key['name']] = key['graphid']
                all_graph = [i['name'] for i in res['result']]
                make_graph = ['Cpu_Load','CPU_Used','Mysql_RW','MySQL_Thread','Network','Network_MySQL','Seconds_Behind_Master','Tcp_conect','Memory','Disk space usage /','Disk space usage /export']
                for aa in make_graph:
                    if graph.has_key(aa):
                        graph.pop(aa)
                #print graph.keys()
                self.delete_graph(graph.values())

    def add_graph(self,hostlist,graph_name,key_,screenids,group_name=''):
        if not group_name:
            group_hostsid = []
            for host in hostlist:
                hostid = self.get_hostid(host)
                if hostid != '0':
                    group_hostsid.append(hostid)
            if len(group_hostsid) == 0:
                group_hostsid = '0'
        else:
            group_hostsid = self.get_group_hosts(group_name)
        if key_[0] == 'mysql.qps':
            graphtype = 1
        else:
            graphtype = 0
        if group_hostsid != '0':
            #group_hostsid.sort()
            gitems = []
            items_sorted = 0
            for hostid in group_hostsid:
                items = {}
                color = "".join([random.sample('0123456ABCDEF',1)[0] for i in range(6)])#颜色随机取RGB
                itemid = self.get_itemid(hostid,key_[0])
                if itemid != '0':
                    items["itemid"] = itemid
                    items["sortorder"] = str(items_sorted)
                    items["color"] = color
                    items["yaxisside"] = 0
                    gitems.append(items)
                    items_sorted = items_sorted + 1
                else:
                    try:
                        itemid = self.get_itemid(hostid,key_[1])
                        if itemid != '0':
                            items["itemid"] = itemid
                            items["sortorder"] = str(items_sorted)
                            items["color"] = color
                            items["yaxisside"] = 0
                            gitems.append(items)
                            items_sorted = items_sorted + 1
                    except:
                        pass
            data = json.dumps(
                {
                    "jsonrpc": "2.0",
                    "method": "graph.create",
                    "params": {
                        "name": graph_name,
                        "width": 900,
                        "height": 200,
                        "graphtype": graphtype,#0：折线图，1：填充图，2：饼状图
                        "show_triggers": 0,#图中显示triggers为1，不显示为0
                        "gitems": gitems
                    },
                    "auth": self.authID,
                    "id": 1
                })
            res = self.get_data(data)
            if res.has_key('error'):
                print "Create graph failed,%s" % res['error']['data']
            else:
                print "Create graph success,graphid is %s" % res['result']['graphids'][0]
                screenids[graph_name] = res['result']['graphids'][0]
        else:
            print "Cannot find this group %s,please Check !" % group_name

    def add_screen(self,graph_name,screenitems):
        screenid = self.getdel_screen(graph_name)
        if screenid != '0':
            self.delete_screen(screenid)
        data = json.dumps(
                {
                "jsonrpc": "2.0",
                "method": "screen.create",
                "params": {
                    "name": graph_name,
                    "hsize": 2,
                    "vsize": 4,
                    "screenitems": screenitems
                },
                "auth": self.authID,
                "id": 1
            })
        res = self.get_data(data)
        #print res
        if res.has_key('error'):
            print "Create screen failed,%s" % res['error']
        else:
            print "Create screen success,graphid is %s" % res['result']

    def delete_graph(self,graphids):
        data = json.dumps(
            {
                "jsonrpc": "2.0",
                "method": "graph.delete",
                "params": graphids,
                "auth": self.authID,
                "id": 1
            })
        res = self.get_data(data)
        '''if res.has_key('error'):
            print "Delete graph Failed: %s" % res['error']
        else:
            print "Delete graph success !"'''

    def delete_screen(self,screenids):
        data = json.dumps(
                {
            "jsonrpc": "2.0",
            "method": "screen.delete",
            "params": [screenids],
            "auth": self.authID,
            "id": 1
        })
        res = self.get_data(data)
        if res.has_key('error'):
            print "Delete screen Failed: %s" % res['error']
        else:
            print "Delete screen success !"

    def delete_host(self,hostip):
        hostid = self.get_hostid(hostip)
        if hostid != '0':
            data = json.dumps(
                {
                    "jsonrpc": "2.0",
                    "method": "host.delete",
                    "params": [
                        hostid
                    ],
                    "auth": self.authID,
                    "id": 1
                })
            res = self.get_data(data)
            if res.has_key('error'):
                print "Delete host from zabbix Failed !"
            else:
                print "Delete host from zabbix success !"
        else:
            print "Can not find this host %s,Check it !" % hostip

    def monitor_host(self,hostip,statusnum=0):
        hostid = self.get_hostid(hostip)
        #statusnum: 0 开启监控  1 关闭监控
        if hostid != '0':
            data = json.dumps(
                {
                    "jsonrpc": "2.0",
                    "method": "host.update",
                    "params": {
                        "hostid": hostid,
                        "status": statusnum
                    },
                    "auth": self.authID,
                    "id": 1
                })
            res = self.get_data(data)['result']
            if len(res["hostids"]):
                if statusnum == 0:
                    print "Update this host %s to Monitored success !" % hostip
                else:
                    print "Update this host %s to Not Monitored success !" % hostip
            else:
                print "Update this host %s Failed !" % hostip
        else:
            print "Can not find this host %s,Check it !" % hostip

    def monitor_iterm(self,hostip,key_,statusnum=0):
        hostid = self.get_hostid(hostip)
        if hostid != '0':
            itermid = self.get_itemid(hostid,key_)
            if itermid != '0':
                #statusnum: 0 开启监控  1 关闭监控
                data = json.dumps(
                    {
                        "jsonrpc": "2.0",
                        "method": "item.update",
                        "params": {
                            "itemid": itermid,
                            "status": statusnum
                        },
                        "auth": self.authID,
                        "id": 1
                    })
                res = self.get_data(data)['result']
                if len(res["itemids"]):
                    if statusnum == 0:
                        print "Update this iterm %s to Monitored success !" % key_
                    else:
                        print "Update this iterm %s to Not Monitored success !" % key_
                else:
                    print "Update this iterm %s Failed !" % key_
            else:
                print "Can not find this iterm %s,Check it !" % key_
        else:
            print "Can not find this host %s,Check it !" % hostip

def select_host():
    try:
        conn = MySQLdb.connect('192.168.137.100',port = 3306,user =  'hvip',passwd =  'yvhkfhvk_wubi')
        cursor = conn.cursor()
        sql = 'select distinct(vip) from jdmysqlmgrsys.mgr_vip where state=2 or state=1'
        cursor.execute(sql)
        alldata = cursor.fetchall()
        cursor.close()
        conn.close()
        return alldata
    except Exception,e:
        print e
        return '0'

def zabbix_host(group_name,flag):
    try:
        conn = MySQLdb.connect('zabbixm.mysql.jddb.com',port = 3358,user =  'zabbix',passwd =  'zabbixmonitor')
        cursor = conn.cursor()
        if flag == 'M':
            sql = "SELECT b.ip FROM zabbix.hosts a,zabbix.interface b,zabbix.hosts_groups c,zabbix.groups d WHERE a.hostid=b.hostid AND a.hostid=c.hostid AND c.groupid=d.groupid AND d.name='%s' AND (b.ip LIKE '10.187.%%' OR b.ip LIKE '10.191.%%' OR b.ip LIKE '172.20.%%' OR b.ip LIKE '172.28.%%' OR b.ip LIKE '10.190.%%') AND a.host like '%%-M-%%' order by b.ip;" % (group_name)
        elif flag == 'S':
            sql = "SELECT b.ip FROM zabbix.hosts a,zabbix.interface b,zabbix.hosts_groups c,zabbix.groups d WHERE a.hostid=b.hostid AND a.hostid=c.hostid AND c.groupid=d.groupid AND d.name='%s' AND (b.ip LIKE '10.187.%%' OR b.ip LIKE '10.191.%%' OR b.ip LIKE '172.20.%%' OR b.ip LIKE '172.28.%%' OR b.ip LIKE '10.190.%%') AND a.host NOT like '%%-M-%%' order by b.ip;" % (group_name)
        elif flag == 'LF':
            sql = "SELECT b.ip FROM zabbix.hosts a,zabbix.interface b,zabbix.hosts_groups c,zabbix.groups d WHERE a.hostid=b.hostid AND a.hostid=c.hostid AND c.groupid=d.groupid AND d.name='%s' AND (ip like '172.20.%%' or ip like '10.191.%%' OR b.ip LIKE '10.190.%%') AND a.host like '%%-S-%%' order by b.ip;" % group_name
        else:
            sql = "SELECT b.ip FROM zabbix.hosts a,zabbix.interface b,zabbix.hosts_groups c,zabbix.groups d WHERE a.hostid=b.hostid AND a.hostid=c.hostid AND c.groupid=d.groupid AND d.name='%s' AND (b.ip LIKE '10.187.%%' OR b.ip LIKE '10.191.%%' OR b.ip LIKE '172.20.%%' OR b.ip LIKE '172.28.%%' OR b.ip LIKE '10.190.%%') order by b.ip;" % group_name
        #print sql
        cursor.execute(sql)
        alldata = cursor.fetchall()
        cursor.close()
        conn.close()
        return alldata
    except Exception,e:
        print e
        return '0'

def get_port(host):
    portlist = [3358,3306,3359,3360,3361,10086]
    mysqlport = 0
    socket.setdefaulttimeout(3)
    for port in portlist:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host, port))
            s.close()
            mysqlport = port
            break
        except socket.error, msg:
            pass
    return mysqlport

def to_log(text,group_name):
    logfile = "log/%s.log" % group_name
    #now = time.strftime("%Y-%m-%d %H:%M:%S")
    tt = str(text) + "\n"
    f = open(logfile,'a+')
    f.write(tt)
    f.close()

def To_zabbix(host):
    group_name = 'VIP'
    proxyname = "(no proxy)"
    hostname = str(host)+'-VIP'
    if mysqlport == '0':
        to_log(host)
    else:
        templates = 'ICMP Ping,Port_%s' % mysqlport
        to_log(str(hostname)+'\t'+str(mysqlport))
        zabbix = zabbixtools()
        zabbix.add_host(hostname,host,group_name,proxyname,templates)

def screen_items(screenids):
    allitems = []
    for key in screenids:
        if '_QPS' in key:
            allitems.append({"resourcetype": 0,"resourceid": screenids[key],"rowspan": 0,"colspan": 0,"dynamic": 1,"x": 0,"y": 0,"height": 100,"width": 500})
        elif '_Network' in key:
            allitems.append({"resourcetype": 0,"resourceid": screenids[key],"rowspan": 0,"colspan": 0,"dynamic": 1,"x": 1,"y": 0,"height": 100,"width": 500})
        elif 'CPU_load' in key:
            allitems.append({"resourcetype": 0,"resourceid": screenids[key],"rowspan": 0,"colspan": 0,"dynamic": 1,"x": 0,"y": 1,"height": 100,"width": 500})
        elif '_CPU_idle' in key:
            allitems.append({"resourcetype": 0,"resourceid": screenids[key],"rowspan": 0,"colspan": 0,"dynamic": 1,"x": 1,"y": 1,"height": 100,"width": 500})
        elif '_Threads' in key:
            allitems.append({"resourcetype": 0,"resourceid": screenids[key],"rowspan": 0,"colspan": 0,"dynamic": 1,"x": 0,"y": 2,"height": 100,"width": 500})
        elif '_Diskutil' in key:
            allitems.append({"resourcetype": 0,"resourceid": screenids[key],"rowspan": 0,"colspan": 0,"dynamic": 1,"x": 1,"y": 2,"height": 100,"width": 500})
        elif '_Seconds_Behind_Master' in key:
            allitems.append({"resourcetype": 0,"resourceid": screenids[key],"rowspan": 0,"colspan": 0,"dynamic": 1,"x": 0,"y": 3,"height": 100,"width": 500})
    return allitems

def todo_creat(graphlist,hostlist,screenids,group_name):
    print "Screen 汇总图的名字为: %s" % group_name
    zabbix = zabbixtools()
    for host in hostlist:
        zabbix.getdel_graph(host)
    for graph_name in graphlist:
        zabbix.add_graph(hostlist,graph_name,graphlist[graph_name],screenids)
    to_log(str(screenids),group_name)
    screen_get = screen_items(screenids)
    zabbix.add_screen(group_name,screen_get)

def main():
    group_name_aa= sys.argv[1]#'Homesns' #这个名字必须为zabbix所属组的名字
    hostlist = zabbix_host(group_name_aa,'M')
    hostlist = [i[0] for i in hostlist]
    if len(hostlist) > 2:
        hostlist = zabbix_host(group_name_aa,'S')
        hostlist = [i[0] for i in hostlist]
        hostlist.sort() 
        print hostlist
        print '从库服务器数量为: %s' % len(hostlist)
        group_name = group_name_aa + '_S'
        to_log(str(hostlist),group_name)
        graphlist = {group_name+'_Threads':['mysql.Threads_connected'],group_name+'_QPS':['mysql.qps'],group_name+'_Network':['Network.IO','docker.network.total'],group_name+'_CPU_load':['system.cpu.load[,avg1]','docker.cpu.load'],group_name+'_CPU_idle':['system.cpu.util[,idle]','docker.cpu.util'],group_name+'_Diskutil':['io.util','docker.disk.util'],group_name+'_Seconds_Behind_Master':['mysql.Seconds_Behind_Master']}
        screenids = {}
        todo_creat(graphlist,hostlist,screenids,group_name)
##########################################################
        hostlist = zabbix_host(group_name_aa,'M')
        hostlist = [i[0] for i in hostlist]
        hostlist.sort()
        print hostlist
        print '主库服务器数量为: %s' % len(hostlist)
        group_name = group_name_aa + '_M'
        to_log(str(hostlist),group_name)
        graphlist = {group_name+'_Threads':['mysql.Threads_connected'],group_name+'_QPS':['mysql.qps'],group_name+'_Network':['Network.IO','docker.network.total'],group_name+'_CPU_load':['system.cpu.load[,avg1]','docker.cpu.load'],group_name+'_CPU_idle':['system.cpu.util[,idle]','docker.cpu.util'],group_name+'_Diskutil':['io.util','docker.disk.util']}
        screenids = {}
        todo_creat(graphlist,hostlist,screenids,group_name)
    else:
        hostlist = zabbix_host(group_name_aa,'A')
        hostlist = [i[0] for i in hostlist]
        hostlist.sort()
        print hostlist
        print '全部数据库服务器数量为: %s' % len(hostlist)
        group_name = group_name_aa
        to_log(str(hostlist),group_name)
        graphlist = {group_name+'_Threads':['mysql.Threads_connected'],group_name+'_QPS':['mysql.qps'],group_name+'_Network':['Network.IO','docker.network.total'],group_name+'_CPU_load':['system.cpu.load[,avg1]','docker.cpu.load'],group_name+'_CPU_idle':['system.cpu.util[,idle]','docker.cpu.util'],group_name+'_Diskutil':['io.util','docker.disk.util'],group_name+'_Seconds_Behind_Master':['mysql.Seconds_Behind_Master']}
        screenids = {}
        todo_creat(graphlist,hostlist,screenids,group_name)

if __name__ == "__main__":
    main()
