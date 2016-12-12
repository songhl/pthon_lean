import sys
import os
import re
import getopt
import MysqlServer
import HostServer
import json

warning = {} #global variable

def get_struct(host, port, father = ''):
    global warning
    try:
        #m = MysqlServer.mysql_server(host, 'db_a', 'vb7ovwjbyReebzt7Nzor', port, father)
        m = MysqlServer.mysql_server(host, 'monitor', 'EhtRreAyVunYKjXQ', port, father)
    except:
        return False
    try:
        children_ip_list = m.get_children_ip()
    except ValueError, msg:            #if read only error, record in warning list
        if warning.has_key(msg[0]) and msg[1] not in warning.get(msg[0]):
            warning[msg[0]].append(msg[1])
        else:
            warning[msg[0]] = [ msg[1] ]
    for ip in children_ip_list:
        try:
            h = HostServer.host_server(ip)
        except :
            continue
        children_port_list = h.get_potential_port()    
        for p in children_port_list:                         #loop connect different ports
            try:
                #s = MysqlServer.mysql_server(ip, 'db_a', 'vb7ovwjbyReebzt7Nzor', p, m)
                s = MysqlServer.mysql_server(ip, 'monitor', 'EhtRreAyVunYKjXQ', p, m)
            except:
                continue
            if s.get_master_id() == None:
                continue
            if int(s.get_master_id()) == int(m.server_id):
                try:
                    s_children_list = s.get_children_ip()
                except ValueError, msg:           #if read only error, record in warning list, now no exception raised
                    if warning.has_key(msg[0]) and msg[1] not in warning.get(msg[0]):
                        warning[msg[0]].append(msg[1])
                    else:
                        warning[msg[0]] = [ msg[1] ]
                if len(s_children_list) != 0:   #if has children
                    s = get_struct(ip, p, m)
                m.get_child_instance(s)
                break
    return m

def main(host, port):
    if host == '172.16.180.98':
        print 'Can not support MariaDB!'
    m = get_struct(host, port)
    if isinstance(m, MysqlServer.mysql_server):
        if m.father_info != {} and m.double != 1:
            m = main(m.father_info['ip'], m.father_info['port'])
        convert_to_bin_tree(m)
        return m
    else:
        return { 'data': {}, 'warning': host + ':' + str(port) + ' connect error'}

def convert_to_bin_tree(instance):
    children = instance.children.values()
    if len(children) > 0:
        instance.left = children[0]
    for i in range(0, len(children)):
        if i + 1 <= len(children) - 1:
            children[i].right = children[i + 1]
        convert_to_bin_tree(children[i])

def bin_tree(instance):
    print instance.host_ip
    if instance.left != '':
        bin_tree(instance.left)
    if instance.right != '':
        bin_tree(instance.right)

if __name__ == '__main__':
    opts, args = getopt.getopt(sys.argv[1:], "h:P:Sv" )
    opts = dict(opts)
    if not opts.has_key('-P'):
        opts['-P'] = 3358
    m = main(opts['-h'], opts['-P'])
    if not isinstance(m, MysqlServer.mysql_server):
        final = json.dumps(m, indent=2)
        print final
        exit(201)
    if opts.has_key('-v'):
        struct = m.vPrint()
    else:
        struct = m.Print()
    final = { 'data': struct, 'warning': warning}
    final = json.dumps(final, indent=2)
    print final
