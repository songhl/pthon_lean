__author__ = 'wangyakun'
#coding:utf8
import MySQLdb
import MySQLdb.cursors
import DBUtils
import DBUtils.PersistentDB
DICT_AUTH={
    "root":'',
    "monitor":'EhtRreAyVunYKjXQ'
}
EXPLICT_DBS=['checksum','test','information_schema','mysql','performance_schema']
dbconfig_mysql_grant = {
    "host": '127.0.0.1',
    'port': 3358,
    'user': 'root',
    'passwd': '',
    'connect_timeout': 3,
    'charset': 'utf8',
    "cursorclass": MySQLdb.cursors.DictCursor,
    'db': 'mysql_grant'
}

pool = DBUtils.PersistentDB.PersistentDB(
    creator=MySQLdb, maxusage=3, setsession=['set autocommit=1'],
    ping=4, closeable=False, **dbconfig_mysql_grant)
authorized_ip_file='ips.txt'
