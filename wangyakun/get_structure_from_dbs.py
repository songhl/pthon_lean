import json
from copy import deepcopy


def get_tree(nodes):
    masternode = [val for val in nodes if val['master_ip'] == ''][0]

    d = dict()
    for item in nodes:
        ip = item['ip']
        masterip = item['master_ip']
        domain = item['domain']
        if not d.has_key(masterip):
            d[masterip] = {'children': [
                {'ip': ip, 'domain': domain, "children": {}}]}
        else:
            d[masterip]['children'].append(
                {'ip': ip, 'domain': domain, "children": {}})

    def handle(fathers, children):
        for child in deepcopy(children):
            for f in deepcopy(fathers):
                if f == child['ip']:
                    item = [val for val in children if val['ip'] == f][0]
                    item['children'] = deepcopy(d[f])['children']
                    if child['children'] == {}:
                        continue
                    handle(fathers, child['children'])
                    fathers.remove(f)
    masterip_a = masternode['ip']
    fathers = d.keys()
    children = d[masterip_a]['children']
    handle(fathers, children)
    return json.dumps({'ip': masterip_a, 'domain': masternode['domain'], 'children': children}, indent=3)

nodes = [{u'status': 1, u'comment': u'', u'domain': u'smym.mysql.jddb.com', u'level': 0, u'ip': u'10.191.28.72', u'master_ip': u'', u'port': 3358}, {u'status': 1, u'comment': u'', u'domain': u'smysa.mysql.jddb.com', u'level': 1, u'ip': u'10.191.66.106', u'master_ip': u'10.191.28.72', u'port': 3358}, {u'status': 1, u'comment': u'', u'domain': u'symsb.mysql.jddb.com', u'level': 1, u'ip': u'10.191.66.107', u'master_ip': u'10.191.28.72', u'port': 3358}, {u'status': 1, u'comment': u'', u'domain': u'allocatesa.mysql.jddb.com', u'level': 1, u'ip': u'10.191.66.113', u'master_ip': u'10.191.28.72', u'port': 3358}, {u'status': 1, u'comment': u'', u'domain': u'smyse.mysql.jddb.com', u'level': 1, u'ip': u'10.191.66.114', u'master_ip': u'10.191.28.72', u'port': 3358}, {u'status': 1, u'comment': u'', u'domain': u'smysd.mysql.jddb.com', u'level': 1, u'ip': u'10.191.66.115', u'master_ip': u'10.191.28.72', u'port': 3358}, {u'status': 1, u'comment': u'', u'domain': u'smysc.mysqlmjq.jddb.com', u'level': 1, u'ip': u'10.187.4.126', u'master_ip': u'10.191.28.72', u'port': 3358}, {u'status': 1, u'comment': u'', u'domain': u'smysg.mysqlmjq.jddb.com',
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         u'level': 2, u'ip': u'10.187.13.63', u'master_ip': u'10.187.4.126', u'port': 3358}, {u'status': 1, u'comment': u'', u'domain': u'smyse.mysqlmjq.jddb.com', u'level': 2, u'ip': u'10.187.13.59', u'master_ip': u'10.187.4.126', u'port': 3358}, {u'status': 1, u'comment': u'', u'domain': u'smysf.mysqlmjq.jddb.com', u'level': 2, u'ip': u'10.187.13.60', u'master_ip': u'10.187.4.126', u'port': 3358}, {u'status': 1, u'comment': u'', u'domain': u'smysd.mysqlmjq.jddb.com', u'level': 2, u'ip': u'10.187.13.50', u'master_ip': u'10.187.4.126', u'port': 3358}, {u'status': 1, u'comment': u'', u'domain': u'smysi.mysqlmjq.jddb.com', u'level': 2, u'ip': u'10.187.44.242', u'master_ip': u'10.187.4.126', u'port': 3358}, {u'status': 1, u'comment': u'', u'domain': u'smysg.mysql.jddb.com', u'level': 1, u'ip': u'172.20.168.38', u'master_ip': u'10.191.28.72', u'port': 3358}, {u'status': 1, u'comment': u'', u'domain': u'smysf.mysql.jddb.com', u'level': 1, u'ip': u'172.20.168.84', u'master_ip': u'10.191.28.72', u'port': 3358}, {u'status': 1, u'comment': u'', u'domain': u'', u'level': 1, u'ip': u'172.20.151.146', u'master_ip': u'10.191.28.72', u'port': 3358}]

print get_tree(nodes)
