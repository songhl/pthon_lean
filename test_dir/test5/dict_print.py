#!/usr/bin/env python
#coding:utf-8
#time: 2016/5/24 15:13
__author__ = 'songhailong' 
#coding=utf-8

def pretty_dict(obj, indent=' '):
    def _pretty(obj, indent):
        for i, tup in enumerate(obj.items()):
            k, v = tup
            #如果是字符串则拼上""
            if isinstance(k, basestring): k = '"%s"'% k
            if isinstance(v, basestring): v = '"%s"'% v
            #如果是字典则递归
            if isinstance(v, dict):
                v = ''.join(_pretty(v, indent + ' '* len(str(k) + ': {')))#计算下一层的indent
            #case,根据(k,v)对在哪个位置确定拼接什么
            if i == 0:#开头,拼左花括号
                if len(obj) == 1:
                    yield '{%s: %s}'% (k, v)
                else:
                    yield '{%s: %s,\n'% (k, v)
            elif i == len(obj) - 1:#结尾,拼右花括号
                yield '%s%s: %s}'% (indent, k, v)
            else:#中间
                yield '%s%s: %s,\n'% (indent, k, v)
    print ''.join(_pretty(obj, indent))

d = { "root": { "folder2": { "item2": None, "item1": None }, "folder1": { "subfolder1": { "item2": None, "item1": None }, "subfolder2": { "item3": None } } } }
# pretty_dict(d)

print(__file__)
print(192.168.131.238
10.190.68.193)