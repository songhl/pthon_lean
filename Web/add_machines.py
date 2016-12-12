# coding:utf8
import requests
import sys
import re
import os
import time
import json
import getpass
username = raw_input('输入你的用户名:')
password = getpass.getpass('输入你的密码:')
username, password = username.strip(), password.strip()
department = raw_input('请输入一级部门:')
project = raw_input('请输入项目名称:')
# department = '成都研究院'
# project = 'EDM1'
url1 = 'http://172.20.98.180/admin/'
s = requests.Session()
s.get(url1)
token = s.cookies["csrftoken"]
r1 = s.post(url1, data={'password': password,
                        'username': username, 'csrfmiddlewaretoken': token, 'next': "/admin/", 'this_is_the_login_form': '1'})


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


def get_depart_id(department):
    url = """http://172.20.98.180/admin/machines/organize/?t=id&_popup=1"""
    r = s.get(url, stream=True)
    departid = None
    for line in r.iter_lines():
        res = re.search(
            '.*/admin/machines/organize/(?P<id>\d+)/\?.*%s.*' % department.strip(), line, re.I)
        if res:
            departid = res.group('id')
            break
    return (0, departid) if departid else (1, departid)


def get_projectid(project):
    url = """http://172.20.98.180/admin/machines/nagiosinfo/"""
    params = {"q": project.strip(), "_popup": "1", "t": "id"}
    r2 = s.get(url, params=params)
    # print r.text.encode('utf8')
    projectid = None
    rec = re.compile(
        '  +<tr class="grp-row grp-row-even"><th><a href="/admin/machines/nagiosinfo/(?P<id>\d+)/\?.*%s.*' % project.strip())
    for line in r2.text.split('\n'):

        res = rec.search(line.encode('utf8'))
        if res:
            projectid = res.group('id')
            break
    return (0, projectid) if projectid else (1, projectid)


def add_machine(projectid, departid, ip, docker, location='xxx'):
    url3 = 'http://172.20.98.180/admin/machines/machine/add/'
    data = {"csrfmiddlewaretoken": s.cookies['csrftoken'],
            "ip": ip.strip(),
            "vip": "",
            "organize": departid,
            "machine_info": projectid,
            "machine_type": 0,
            "host_type": docker and 1 or 0,  # 1是docker
            "machine_location": location,
            "_save": '保存'
            }
    r3 = s.post(url3, data=data)
    if r3.status_code == 200:
        return 0, ip.strip() + (docker and 'docker' or '物理机')
    else:
        return 1, ip.strip() + (docker and 'docker' or '物理机')

code, departid = get_depart_id(department)
try:
    int(departid)
except:
    print '未找到一级部门!'
    sys.exit(1)
else:
    code, projectid = get_projectid(project)
    try:
        int(projectid)
    except:
        print '未找到项目!'
        sys.exit(1)
    else:
        list_ret = []
        for line in open('mlist'):
            if not line.strip().startswith('#'):
                # try extracting ip,docker,location from file
                try:
                    tmp = line.split(':')
                    ip = tmp[0].strip()
                    docker = tmp[1].strip().lower() == 'docker' or False
                    try:
                        location = tmp[2].strip()
                    except:
                        location = 'xxx'
                except:
                    docker = True
                    location = 'xxx'
                if ipv4(ip):
                    # add machine,report
                    rst = add_machine(
                        projectid, departid, ip, docker, location)
                    list_ret.append(rst)
                else:
                    list_ret.append((1, ip + ' not ipv4'))
        list_success, list_failed = [val[1] for val in list_ret if val[0] == 0], [
            val[1] for val in list_ret if val[0] != 0]
        if list_success:
            print 'success:'
            print '\n'.join(list_success)
            print
        if list_failed:
            print 'failed:'
            print '\n'.join(list_failed)
        print '请检查结果!'