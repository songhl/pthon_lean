# coding:utf8
__author__ = 'wangyakun'
import os
import time
import datetime
import json
import urllib2
import sys
import re
from zabbix_api import ZabbixApi
reload(sys)
sys.setdefaultencoding('utf8')


def ipv4(ip):
    import re
    try:
        str(ip)
    except:
        return False
    if re.match(r"^([0-9]{1,3}\.){3}[0-9]{1,3}$", str(ip)):
        num_list = ip.split(".")
        for i in range(len(num_list)):
            x = range(0, 255)
            if i in [0, 3]:
                x = range(1, 255)
            if int(num_list[i]) not in x:
                return False
        return True
    return False


def ssh_modify_zabbix_hostname(ip, hostname, password):
    cmd = """/bin/sed -i  's/^ *Hostname\=.*/Hostname\=%s/g' /export/data/zabbix/etc/zabbix_agentd.conf&&/etc/init.d/zabbix_agentd stop;/etc/init.d/zabbix_agentd start""" % (
        re.escape(hostname.strip()))
    # print cmd
    zabbix_host_modify_root_password = [('aaa', password.strip())]
    for i, p in enumerate(zabbix_host_modify_root_password):
        password = p[1].strip()
        try:
            return ssh_exec(cmd, ip.strip(), port=22, username='root', password=password, timeout=35, pty=True)
        except Exception, e:
            if i == len(zabbix_host_modify_root_password) - 1:
                raise e
            else:
                continue


def ssh_exec(cmd, hostname, port=22, username='root', password=None, key_filename=None, timeout=5, pty=True):

    import paramiko
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.load_system_host_keys()
    ssh.connect(hostname=hostname, port=port, username=username,
                password=password, key_filename=key_filename, timeout=timeout)
    transport = ssh.get_transport()
    channel = transport.open_session()
    if pty:
        channel.get_pty()
    channel.settimeout(timeout)
    channel.exec_command(cmd)
    stdin = channel.makefile('wb', 10240)
    stdout = channel.makefile('rb', 10240)
    stderr = channel.makefile_stderr('rb', 10240)
    out = stdout.read()
    err = stderr.read()
    retcode = channel.recv_exit_status()
    channel.close()
    ssh.close()
    return retcode, out, err
api_info = {
    'url':  'http://zabbixm.mysql.jddb.com/api_jsonrpc.php',
    'user': 'monitor',
    'password': 'monitor'
}


def call_it(instance, name, args=(), kwargs=None):
    "indirect caller for instance methods and multiprocessing"
    if kwargs is None:
        kwargs = {}
    return getattr(instance, name)(*args, **kwargs)


def action(task, ssh_password, lock):
    ip, hostname, hostname_new, isslave, hostid = task
    try:
        zbxapi = ZabbixApi(api_info)
        zbxapi.login()
        msg = ''
        if not hostname_new.strip():

            msg = '机器名不能为空白'
        else:
            zbxapi.set_hostname(hostid, hostname_new)
            templateid_slave = zbxapi.get_template_id('Mysql_replmonitor')
            if isslave:
                zbxapi.host_add_template(hostid, templateid_slave)
            else:
                zbxapi.host_del_template(hostid, templateid_slave)
            try:
                ret = ssh_modify_zabbix_hostname(
                    ip, hostname_new, ssh_password)
            except Exception, e:
                raise Exception('SSH connection error:%s' % repr(e))
            if type(ret) is tuple and ret:
                if ret[0] != 0:
                    raise Exception('修改agentd配置出错:' + ';'.join(ret[1:]))
            msg = '修改成功！'

    except Exception, e:
        msg = e.message
    lock.acquire()
    print ip, msg
    open('modify.log', 'a+').write('\n%s:%s' %
                                   (time.ctime(), ' '.join([ip, hostname, hostname_new, isslave and 'slave' or 'not slave', hostid])))
    lock.release()
    return msg


class ZabbixHostnameModify:

    def get(self, ip):
        zbxapi = ZabbixApi(api_info)
        zbxapi.login()
        hostname = zbxapi.get_hostname(ip)
        hostname_new = self.transferhostname(hostname)
        isslave = re.match('^.+\-S\-.+$', hostname_new, re.I) and True or False
        hostid = zbxapi.get_hostid(ip)
        return (ip, hostname, hostname_new, isslave, hostid)

    def post(self, list_task, ssh_password):
        import multiprocessing
        from multiprocessing import Pool, Manager
        manager = multiprocessing.Manager()
        lproxy = manager.list()
        lproxy.append(False)
        lock = Manager().Lock()
        count = len(list_task) >= 5 and 5 or len(list_task)
        pool = Pool(processes=count)
        func = action
        async_results = [pool.apply_async(func, args=(task, ssh_password, lock
                                                      )
                                          )
                         for task in list_task]

        pool.close()
        for rr in async_results:
            try:
                rr.wait(timeout=10)

                if rr.successful():
                    pass
            except:
                print 'timeout,please check'

    def transferhostname(self, name):
        return (name.find('-M-') != -1 or name.find('-m-') != -1) and name.replace('-M-', '-S-').replace('-m-', '-S-') or name.replace('-S-', '-M-').replace('-s-', '-M-')


def format_output(ip_task):
    ip, hostname, hostname_new, isslave, hostid = ip_task
    print '#############################################'
    print 'ip:%s\n原主机名:%s\n新主机名：%s\n是否从库：%s' % (ip, hostname, hostname_new, isslave and '是' or '否')


def work(options):
    import getpass
    z = ZabbixHostnameModify()
    password = getpass.getpass(u'请输入主机的root密码：')

    if options.interactive:
        ip = raw_input('IP:')
        (ip, hostname, hostname_new, isslave, hostid) = z.get(ip.strip())
        print '目前的主机名：%s' % hostname
        print '帮你生成的新名：%s' % hostname_new
        confirm = raw_input('可以使用吗（y/n）,"y"确认，"n"进行修改\n')
        if confirm != 'y':
            new = raw_input(u'输入新主机名：')
            hostname_new = new.strip()
        isslave = raw_input(u'是否是从库？（y/n)\n')
        isslave = isslave == 'y'
        ip_task = (ip, hostname, hostname_new, isslave, hostid)
        print '任务详情：'
        format_output(ip_task)
        list_task = [ip_task]

    else:
        list_ip = [val.strip() for val in open(options.filename, 'r')]
        list_ip_task = [z.get(ip.strip())
                        for ip in list_ip if ipv4(ip.strip())]

        for ip_task in list_ip_task:
            format_output(ip_task)
        list_task = list_ip_task
    confirm2 = raw_input(u'开始修改？（y/n)\n')
    if confirm2 == 'y':
        z.post(list_task, password)

    else:
        print '已取消'

if __name__ == '__main__':

    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option(
        "-f", action='store', type='string', dest="filename", default=None)

    parser.add_option("-i", action='store_true', default=False, dest="interactive",
                      help='''交互式''')

    (options, args) = parser.parse_args()
    if options:
        if not options.interactive and not options.filename:

            print '批量操作请指定IP列表文件，使用说明使用--help'
        else:
            work(options)
    else:
        parser.print_help()

