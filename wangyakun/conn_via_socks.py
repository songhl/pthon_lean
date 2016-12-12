# coding:utf8
# author:wangyakun
'''
ssh -fN -D 127.0.0.1:1009 user@[remote|localhost]
'''
from mysqlconn2 import MysqlConnection
import pymysql
# from socks5_plink import *
# from utils import MyThread
import time
proxyport = 1009
import socks
import socket

ra
def create_connection(address, timeout=None, source_address=None):
    sock = socks.socksocket()
    sock.connect(address)
    return sock

socks.setdefaultproxy(proxy_type=socks.PROXY_TYPE_SOCKS5,
                      addr='192.168.1.10', port=int(proxyport), rdns=True)

# patch the socket module
socket.socket = socks.socksocket
socket.create_connection = create_connection

conn = MysqlConnection(host='192.168.1.10', user='root',
                       db='mysql', password='hailong',  port=3358)
# conn=pymysql.connect(host='192.168.1.10',user='root',passwd='hailong',db='mysql',port=3306,charset='utf8')
# cur=conn.cursor()
print proxyport
print conn.execute('show processlist')
# print cur.execute('show processlist')

time.sleep(10)

