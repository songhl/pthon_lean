__author__ = 'wangyakun'
#coding:utf8
import sys,os
from config import DICT_AUTH,pool,EXPLICT_DBS
import MySQLdb.cursors
from MySQLdb import escape_string
def ipv4(ip):
    import re
    try:
        str(ip)
    except:
        return False
    if re.match(r"^([0-9]{1,3}\.){3}[0-9]{1,3}$", str(ip)):
        num_list = ip.split(".")
        for i in range(len(num_list)):
            x = range(0, 256)
            if int(num_list[i]) not in x:
                return False
        return True
    return False
def mylogger(file=None, level='debug'):
    u'''
    modified on 2013.1.11
    this function return a logging.RootLogger object,
    which uses function error(str) or exception(e)
    for recording your log in file
    '''
    import logging
    if file is None:
        return logging
    LEVELS = {'debug': logging.DEBUG, 'info': logging.INFO,
              'warning': logging.WARNING, 'error': logging.ERROR, 'critical': logging.CRITICAL}
    logger = logging.getLogger()
    formatter = logging.Formatter(
        '%(asctime)s %(threadName)s %(funcName)s line:%(lineno) -8s%(levelname)-8s %(message)s ', ' %Y-%m-%d %H:%M:%S')
    try:
        file_handler = logging.FileHandler(file)
    except Exception, e:
        print 'log failed',e
        return None
    else:
        file_handler.setFormatter(formatter)
        stream_handler = logging.StreamHandler(sys.stderr)
        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)
        logger.setLevel(LEVELS.get(level))
    #logger.removeHandler(stream_handler)  # debug(indicate to eclipse)
    return logger
try:
    logger=mylogger(file='/var/log/grant/grant.log')
except:
    logger = mylogger(file=os.path.join(os.path.basename(__file__),'grant.log'))

def ssh_exec(cmd, hostname, port=22, username='root', password=None, key_filename=None, timeout=5, pty=True):

    import paramiko
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.load_system_host_keys()
    ssh.connect(hostname=hostname, port=port, username=username,
                password=password, key_filename=key_filename, timeout=timeout)
    transport = ssh.get_transport()
    channel = transport.open_session()
    if pty:channel.get_pty()
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
def sendmail(to_list, cc_list, sub='test', content='testttt'):


    # mail_host = "58.83.206.59"
    mail_host = "172.17.27.249"
    mail_user = 'mysqlyw'
    mail_pass = "ds4zy8zAinwmQvf_1"
    mail_postfix = "jd.com"
    me = mail_user + "<" + mail_user + "@" + mail_postfix + ">"
    msg = MIMEText(content, _charset='utf-8')
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = ";".join(to_list)
    msg['Cc'] = ";".join(cc_list)
    s = smtplib.SMTP()
    s.connect(mail_host, 25)
    # s.login(mail_user, mail_pass)
    s.sendmail(me, to_list+cc_list, msg.as_string())
    s.close()
    return 0
class MysqlConnectionPool():

    def __init__(self, pool):
        self.pool = pool

    def connection(self, persist=True):
        conn = persist and self.pool.connection() or self.pool.steady_connection()
        return conn

    def execute(self, sql, args):
        conn = self.connection()
        cur = conn.cursor(MySQLdb.cursors.DictCursor)
        cur.execute(sql, *args)
        ret = cur.fetchall()
        cur.close()
        conn.close()
        return ret

    def executemany(self, sql, *args):
        conn = self.connection()
        cur = conn.cursor(MySQLdb.cursors.DictCursor)
        ret = cur.executemany(sql, *args)
        cur.close()
        conn.close()
        return ret

    def query(self, sql, *args):
        return self.execute(sql, *args)

    def get(self, query, *parameters):
        rows = self.execute(query, *parameters)
        if not rows:
            return None
        elif len(rows) > 1:
            raise Exception("Multiple rows returned for Database.get() query")
        else:
            return rows[0]


conn_ = MysqlConnectionPool(pool)

class DbModel(object):
    def __init__(self,host,port,database=None,priv=None,dbuser=None):
        self._host=host
        self._port=port
        self._database=database
        self._priv=priv
        self._dbuser=dbuser
        self._manage_user='monitor'
        self.gen_cursor()

    def __del__(self):
        try:
            cur.close()
            conn.close()
        except:
            pass
    def gen_cursor(self):
        self.conn = MySQLdb.connect(host=self._host, port=int(self._port), user=self._manage_user, passwd=DICT_AUTH[self._manage_user], connect_timeout=3)
        self.cur = self.conn.cursor(MySQLdb.cursors.DictCursor)

    def execute(self,sql,args=None):
        self.cur.execute(sql, args)
        rs = self.cur.fetchall()
        self.conn.commit()

        return rs

    def get_dbs(self):
        sql='''show databases;'''
        dbs=self.execute(sql=sql)
        dbs=[val['Database'] for val in dbs if val['Database'].lower() not in EXPLICT_DBS]
        return dbs
    def check_db_exists(self,db):
        return db.strip() in self.get_dbs()
    def get_users(self):

        if not self.check_db_exists(self._database):
            raise Exception('database:{0} not exists'.format(self._database))
        def __gen_new_username():
            return len(self._database)>13 and self._database[:13]+'_'+self._priv.lower() or self._database+'_'+self._priv.lower()
        if self._priv not in ['rw', 'ro', 'sj', 'cx', 'dw']:
            raise Exception('only rw and ro is accepted')
        sql = 'select distinct user from mysql.db where db = "%s" and user like "%%_%s"'%(escape_string(self._database),escape_string(self._priv))
        list_user = [ i['user'] for i in self.execute(sql=sql)]
        if not list_user:
            is_new=1
            new_name=__gen_new_username()
            list_user=[new_name]
        else:
            is_new=0
        return is_new,list_user

    def get_referip(self):
        list_referip= []
        sql = '''select count(distinct u.password) as num
                FROM
                  mysql.user u,
                  mysql.db d
                WHERE u.user = d.`User`
                  AND d.db = %s
                  AND u.user = %s '''
        count= self.execute(sql=sql,args=[self._database,self._dbuser])
        count=count[0]['num']
        if count> 1:
            sql = 'select distinct user, host  from mysql.user where user = %s'
            ret= self.execute(sql=sql,args=[self._dbuser])
            list_referip = list(set([i['host'] for i in ret]))
        elif count==0:
            list_referip=None
        return list_referip

    def grant(self):
        pass



