# coding:utf8
import os
import json
import re
import urllib
import urllib2


class ZabbixApi:

    def __init__(self, api_info):
        self.api_info = api_info
        self.header = {"Content-Type": "application/json-rpc"}
        self.data = {"jsonrpc": "2.0", "method": "apiinfo.version",
                     "id": 1, "auth": None, "params": {}}

    def login(self):
        self.data['method'] = 'user.login'
        self.data['params'] = {
            'user': self.api_info['user'],
            'password': self.api_info['password']
        }
        response = self.request()
        self.data['auth'] = response['result']
        self.data['id'] = 1

    def request(self):
        url = self.api_info['url']
        postdata = json.dumps(self.data)
        req = urllib2.Request(url, postdata)

        for k, v in self.header.items():
            req.add_header(k, v)
        try:
            result = urllib2.urlopen(req)
        except urllib2.URLError as e:
            raise e
        else:
            response = json.loads(result.read())
            result.close()
            return response

    def openapi(self, method, params):
        self.data['method'] = method
        self.data['params'] = params
        return self.request()

    def get_xxx(self, method, params, resultkey):

        ret = self.openapi(method, params)
        try:
            result = ret['result'][0]
            if result[resultkey] == "0":
                raise Exception('%s not found' % resultkey)
            return result[resultkey]
        except KeyError:
            raise Exception('%s not found' % resultkey)
        except IndexError:
            raise Exception('%s not found' % resultkey)

    def get_hostid(self, hostip):
        method = "host.get"
        params = {
            "output": ["name", "status", "host", "groups"],
            "output": "extend",
            "selectGroups": "extend",
            "filter": {"ip": [hostip]}
        }
        return self.get_xxx(method, params, resultkey='hostid')

    def get_hostname(self, hostip):
        method = "host.get"
        params = {
            "output": ["name", "status", "host", "groups"],
            "output": "extend",
            "selectGroups": "extend",
            "filter": {"ip": [hostip.strip()]}
        }
        return self.get_xxx(method, params, resultkey='host')

    def set_hostname(self, hostid, hostname):

        # hostid = self.get_hostid(hostip.strip())
        # statusnum: 0 开启监控  1 关闭监控
        method = "host.update"
        params = {
            "hostid": hostid,
            "host": hostname.strip(),
            "name": ""
        }
        return self.set_xxx(method, params)

    def get_itemid(self, hostip, key_):
        hostid = self.get_hostid(hostip)
        method = 'item.get'
        params = {
            "output": "extend",
            "hostids": hostid,
            "search": {
                "key_": key_
            },
            "sortfield": "name"
        }
        return self.get_xxx(method, params, resultkey='itemid')

    def item_delete(self, hostip, key_):
        itemid = self.get_itemid(hostip, key_)
        method = 'item.delete'
        params = ["%s" % str(itemid)]
        return self.get_xxx(method, params, resultkey='itemids')

    def set_xxx(self, method, params):

        ret = self.openapi(method, params)
        if ret.has_key('error'):
            raise Exception(
                '%s error:%s' % (method, ret['error']["message"] + ":" + ret['error']['data']))
        return 0

    def set_host_monitored(self, hostip, state):

        hostid = self.get_hostid(hostip)
        # statusnum: 0 开启监控  1 关闭监控
        method = "host.update"
        params = {
            "hostid": hostid,
            "status": state
        }
        return self.set_xxx(method, params)

    def get_triggerid(self, hostip, key):
        itemid = self.get_itemid(hostip, key)
        method = 'trigger.get'
        params = {
            "itemids": itemid,
            "output": "extend",
            "selectFunctions": "extend"
        }

        return self.get_xxx(method, params, resultkey='triggerid')

    def get_shl(self, hostip):
        # itemid = self.get_itemid(hostip, key)
        method = 'trigger.get'
        params = {
             "group": "Mysql",
            "output": "extend",
            "selectFunctions": "extend"
        }

        return self.get_xxx(method, params, resultkey='triggerid')
    def set_trigger_monitored(self, hostip, key, state=0):

        triggerid = self.get_triggerid(hostip, key)
        # statusnum: 0 开启监控  1 关闭监控
        method = "trigger.update"
        params = {
            "triggerid": triggerid,
            "status": state
        }
        return self.set_xxx(method, params)

    def get_template_id(self, templatename):
        method = 'template.get'
        params = {
            "output": "extend",
            "filter": {
                "host": [
                    "%s" % templatename,
                ]
            }
        }
        return self.get_xxx(method, params, resultkey='templateid')

    def host_add_template(self, hostid, templateid):
        method = "host.massadd"

        params = {
            "templates": [
                {
                    "templateid": "%d" % int(templateid)
                }
            ],
            "hosts": [
                {
                    "hostid": "%d" % int(hostid)
                }
            ]
        }
        return self.set_xxx(method, params)

    def host_del_template(self, hostid, templateid):

        method = "host.massremove"
        params = {
            # "templateids": "%d"%int(templateid),
            "templateids_clear": "%d" % int(templateid),
            "hostids": ["%d" % int(hostid)]
        }
        return self.set_xxx(method, params)

if __name__ == '__main__':
    api_info = {
        'url':  'http://zabbixm.mysql.jddb.com/api_jsonrpc.php',
        'user': '',
        'password': ''
    }
    zbx = ZabbixApi(api_info)

