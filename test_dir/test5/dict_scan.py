#!/usr/bin/env python
#coding:utf-8
#time: 2016/5/23 14:45
__author__ = 'songhailong' 
person = {"male":{"name":"Shawn"},"female":{"name":"Betty","age":23},"children":{"name":{"first_name":"李","last_name":{"old":"明明","now":"铭"}},"age":4}}


def list_all_dict(dict_a):
    if isinstance(dict_a,dict) : #使用isinstance检测数据类型
        for x in range(len(dict_a)):
            temp_key = dict_a.keys()[x]
            temp_value = dict_a[temp_key]
            print("%s : %s" %(temp_key,temp_value))
            list_all_dict(temp_value) #自我调用实现无限遍历
list_all_dict(person)

def print_tree(tree):
    for k, v in tree.items():
        if isinstance(v, dict):
            print_tree(v)
        else:
            print(k)