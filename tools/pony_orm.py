#!/usr/bin/env python
#coding:utf-8
#time: 2016/7/19 14:40
__author__ = 'songhailong' 
from pony.orm import *
db = Database("mysql", host="192.168.1.82", user="root", passwd="",db="pony")
class Customer(db.Entity):
    name = Required(str)
    picture = Optional(buffer)

sql_debug(True)
db.generate_mapping(create_tables=True)
