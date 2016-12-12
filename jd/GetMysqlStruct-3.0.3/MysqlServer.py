import MySQLdb

def proc_filter(x): return ( x['Command'] == 'Binlog Dump' or \
                    x['Command'] == 'Binlog Dump GTID') and \
                     x['User'] == 'replicater'

class mysql_server(object):
    def __init__(self, server, user, password, port, father = ''):
        self.host_ip = server
        self.port = port
        self.conn = MySQLdb.connect(\
            host = server,\
            user = user,\
            passwd = password,\
            port = int(port),\
            db = 'mysql'\
        )
        self.cursor = self.conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        self.cursor_list = self.conn.cursor()
        self.father = father
        self.double = 0
        self.left = ''
        self.right = ''
        self.server_id = self.get_server_id()
        self.read_only = self.get_read_only()
        self.slave_status = self.get_slave_status()
        self.processlist = self.get_processlist()
        self.father_info = self.get_father_info()
        self.children = {}

    def execute_list(self, sql):
        try:
            self.cursor_list.execute(sql)
        except Exception, msg:
            print msg[1]

    def execute(self, sql):
        try:
            self.cursor.execute(sql)
        except Exception, msg:
            print msg[1]

    def get_rml(self):
        s = self.get_slave_status()
        master_log = s['Master_Log_File']
        return master_log

    def get_rmlp(self):
        s = self.get_slave_status()
        rml_pos = s['Read_Master_Log_Pos']
        return rml_pos

    def rollback(self):
        try:
            self.conn.rollback()
        except:
            print 'rollback error'

    def commit(self):
        try:
            self.conn.commit()
        except:
            print 'commit error'

    def set_slave(self, stat):
        if stat != 'start' and stat != 'stop':
            print 'slave status can only be start or stop'
            exit(1)
        sql = '%s slave' % stat
        print '%s: %s slave' % (self.host_ip, stat)
        self.execute(sql)

    def get_processlist(self):
        sql = 'show processlist'
        self.execute(sql)
        s = self.cursor.fetchall()
        return s

    def get_slave_status(self):
        sql = 'show slave status'
        self.execute(sql)
        s = self.cursor.fetchone()
        return s

    def set_father(self, instance):
        self.father = instance

    def get_father_info(self):
        father_info = {}
        if not self.slave_status:
            return father_info
        if self.slave_status['Slave_IO_Running'] != 'Yes' or \
        self.slave_status['Slave_SQL_Running'] != 'Yes':
            father_info = {}
        else:
            father_info['ip'] = self.slave_status['Master_Host']
            father_info['port'] = self.slave_status['Master_Port']
            father_info['server_id'] = self.slave_status['Master_Server_Id']
        return father_info

    def get_server_id(self):
        sql = '''show variables like '%server_id%' '''
        self.execute(sql)
        i = self.cursor.fetchone()
        return i['Value']

    def get_master_id(self):
        return self.father_info.get('server_id')

    def get_read_only(self):
        sql = '''show variables like '%read_only%' '''
        self.execute(sql)
        r = self.cursor.fetchone()
        return r['Value']

    def set_read_only(self, stat):
        if stat != 'ON' and stat != 'OFF':
            print 'variable read_only can only be ON or OFF'
            exit(1)
        sql = 'set global read_only = %s' % stat
        print '%s: setting read_only %s' % (self.host_ip, stat)
        self.execute(sql)

    def get_children_ip(self):
        children = filter(proc_filter, self.processlist)
        children_ip = [ (i['Host'].split(':'))[0] for i in children ]
        if self.check_read_only() in children_ip:
            children_ip.remove(self.check_read_only())
        return children_ip

    def get_child_instance(self, instance):
        self.children[instance.host_ip] = instance

    def check_read_only(self):
        if self.father != '' and self.read_only == 'OFF':
            if self.father.get_master_id() and \
            int(self.father.get_master_id()) == int(self.server_id):
                self.double = 1
                self.father.double = 1
                return self.father.host_ip.strip()
            else:
                #raise ValueError(self.host_ip, 'read_only error')
                #print self.host_ip, 'read_only error'
                pass
        return True

    def vPrint(self):
        struct = {}
        struct['name'] = self.host_ip
        struct['port'] = str(self.port)
        if self.father != '':
            struct['father'] = self.father.host_ip + ':' + str(self.father.port)
        else:
            struct['father'] = ''
        if len(self.children) != 0:
            struct['children'] = []
            for item in self.children.items():
                struct['children'].append(item[1].vPrint() )
        return struct

    def Print(self):
        struct = {}
        struct[self.host_ip + ':' + str(self.port)] = {}
        if len(self.children) != 0:
            for item in self.children.items():
                struct[self.host_ip + ':' + str(self.port)][item[1].host_ip + ':' + str(item[1].port)] = \
                (item[1].Print().values())[0]
        return struct

    def find(self, ip):
        if ip == self.host_ip:
            return self
        else:
            for c in self.children.values():
                i = c.find(ip)
                if isinstance(i, mysql_server):
                    return i

if __name__ == '__main__':
    p = mysql_server('192.168.137.100', 'monitor', 'EhtRreAyVunYKjXQ', 3306)
