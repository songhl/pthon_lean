#!/usr/bin/env python
#coding:utf-8
__author__ = 'songhailong'
import mysql.connector

config={'host':'192.168.1.10',
        'user':'root',
        'password':'hailong',
        'port':3358,
        'database':'test',
        'charset':'utf8'}
try:
    cnn=mysql.connector.connect(**config)
except mysql.connector.Error as e:
    print('connect fails!{}'.format(e))
cur = conn.cursor()