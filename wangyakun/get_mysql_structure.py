# coding:utf8
import sys
import time
reload(sys)
sys.setdefaultencoding('utf8')
import multiprocessing
from multiprocessing import Pool, Manager, Queue, Process, Lock
# from mysqlconn2 import dbconfig,MysqlConnection
import MySQLdb
import _mysql_exceptions


def call_it(instance, name, args=(), kwargs=None):
    "indirect caller for instance methods and multiprocessing"
    if kwargs is None:
        kwargs = {}
    return getattr(instance, name)(*args, **kwargs)


class GetMysqlStructure(object):

    def __init__(self, host, port, username, password):
        self._host = host
        self._port = int(port)
        self._username = username
        self._password = password
        self._manager = Manager()
        self._lock = self._manager.Lock()
        self._dict_result = self._manager.dict()

    def gen_cursor(self, host, port):
        conn = MySQLdb.connect(
            host=host, port=port, user=self._username, passwd=self._password, connect_timeout=3)
        cur = conn.cursor(MySQLdb.cursors.DictCursor)
        return conn, cur

    def execute(self, host, port, sql, args=None):
        conn, cur = self.gen_cursor(host, port)
        cur.execute(sql, args)
        rs = cur.fetchall()
        cur.close()
        conn.commit()
        return rs

    def get_master_instance(self):
        def __get_close_father(host_tt, port_tt):
            sql = 'show slave status'
            ret = self.execute(host_tt, port_tt, sql)
            if not ret:
                return host_tt, port_tt
            else:
                return ret[0]['Master_Host'], ret[0]['Master_Port']

        cur_host = self._host
        cur_port = self._port
        while 1:
            try:

                cur_host_t, cur_port_t = __get_close_father(cur_host, cur_port)
                if cur_host_t == cur_host and cur_port_t == cur_port or cur_host_t.startswith('1.1.'):
                    break
                else:
                    cur_host, cur_port = cur_host_t, cur_port_t
            except Exception, e:
                return 1, 'connect to {host}:{port} error:{error}'.format(host=cur_host, port=cur_port, error=str(e))

        return 0, (cur_host, cur_port)

    def get_child_instance(self, queue, dict_result, lock, manager):
        def __confirm_slave(host_t, port_t, serverid_t):
            sql = 'show global variables like "server_id"'
            try:
                rr = self.execute(host_t, port_t, sql)
            except _mysql_exceptions.OperationalError:
                return False
            else:
                if rr:
                    serverid_real = rr[0]['Value']
                    if int(serverid_real) == int(serverid_t):
                        return True
                    else:
                        return False
                else:
                    # raise Exception('slave %s:%d does not have
                    # serverid!!!'%(host_t,port_t))
                    return False
        while 1:
            time.sleep(0.2)
            if queue.qsize() == 0:
                break
            master_host_t, master_port_t = queue.get()
            sql1 = 'show slave hosts'
            sql2 = "select host as Host from information_schema.processlist where command like 'binlog dump';"
            ret1 = self.execute(master_host_t, master_port_t, sql1)
            ret1 = list(ret1)
            ret2 = self.execute(master_host_t, master_port_t, sql2)
            list_slave_host = [val['Host'].split(':')[0] for val in ret2]
            # print 'list_slave_host', list_slave_host, master_host_t,
            # master_port_t
            for host in list_slave_host:
                for item in ret1:
                    serverid = item['Server_id']
                    port = item['Port']
                    confirm = __confirm_slave(host, port, serverid)

                    if confirm:
                        ret1.remove(item)
                        lock.acquire()

                        # go on get slaves
                        queue.put((host, port))

                        # summery result
                        key = '%s:%d' % (master_host_t, master_port_t)
                        # print key, dict_result.has_key(key)
                        if dict_result.has_key(key):
                            lll = dict_result[key]
                            lll.append((host, port))
                            dict_result[key] = lll
                            # print dict_result, host, port
                        else:
                            list_t = manager.list()
                            # list_t = list()
                            list_t.append((host, port))
                            dict_result[key] = list_t
                        lock.release()

    def gen_structure(self):
        ret, master = self.get_master_instance()
        if ret == 1:
            print 'error', master
        else:
            self.master_host, self.master_port = master
            _queue = self._manager.Queue(50)
            _queue.put(
                (self.master_host, self.master_port)
            )
            list_process = []
            for i in range(5):

                p = Process(target=self.get_child_instance, args=(
                    _queue, self._dict_result, self._lock, self._manager))
                list_process.append(p)
                p.start()
                p.join()
        print 'self._dict_result', self._dict_result


if __name__ == '__main__':
    # 5.5.14
    s = GetMysqlStructure(host='172.20.81.157', port=3306,
                          username='g_auto', password='0nE=*B9g^d4S')
    s.gen_structure()
    # 5.5.38
    s = GetMysqlStructure(host='172.28.141.53', port=3358,
                          username='g_auto', password='0nE=*B9g^d4S')

    s.gen_structure()
