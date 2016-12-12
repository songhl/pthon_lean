#!/usr/bin/env python
#coding:utf-8
#time: 2016/1/21 17:45
__author__ = 'songhailong' 
storage={}
storage['first']={}
storage['middle']={}
storage['last']={}
me='Magnus Lie Hetland'
storage['first']['Mangus']=[me]
storage['middle']['Lie']=[me]
storage['last']['Hetland']=[me]
print(storage['middle']['Lie'])

my_sister='Anne Lie Hetland'
storage['first'].setdefault('Anne',[]).append(my_sister)
storage['middle'].setdefault('Lie',[]).append(my_sister)
storage['last'].setdefault('Hetland',[]).append(my_sister)
print(storage['first']['Anne'])
print(storage['middle']['Lie'])
######################################################
#def init(data):
#    data['first']={}
#    data['middle']={}
#    data['last']={}
#storage={}
#init(storage)
#print(storage)
#######################################################

print(storage['middle'].get('Lie'))
print(storage['middle']['Lie'])
def lookup(data,label,name):
    return data[label].get(name)
lookup(storage,'middle','Lie')

def store(data,full_name):
    names=full_name.split()
    if len(names) == 2:names.insert(1,'')
    labels='first','middle','last'
    for label,name in zip(labels,names):
        people=lookup(data,label,name)
        if people:
            people.append(full_name)
        else:
            data[label][name]=[full_name]


