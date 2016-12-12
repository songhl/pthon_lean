import class_connect3
import re
import sys

def port_filter(x): return  re.search(r'LISTEN', x) and \
                    re.search(r'mysql', x) and not\
                     re.search(r'STREAM', x)

class host_server(class_connect3.Mysql_connect2):
    def __init__(self, ip):
        type = 'os'
        c_user = 'root'
        c_pass = 'a'
        self.vip = ''
        super(host_server, self).__init__(ip,type,c_user,c_pass)

    def execute(self, cmd, r = ''):
        self.stdin,self.stdout,self.stderr = self.ssh.exec_command(cmd)
        if r == 'scalar':
            out = self.stdout.readline()
        else:
            out = self.stdout.readlines()
        return out

    def get_potential_port(self):
        cmd = r'netstat -anp'
        o = self.execute(cmd)
        o = filter(port_filter, o)
        o = [ re.search(r':(\d{4})', (i.split())[3]).group(1) for i in o ]
        return o

if __name__ == '__main__':
    p = host_server('172.26.10.61')
    print p.get_potential_port()
