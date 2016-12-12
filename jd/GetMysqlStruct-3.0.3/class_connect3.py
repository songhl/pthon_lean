#!/usr/bin/python   
#-*- coding: utf-8 -*-  
import paramiko  
import threading  
import sys
import os
import re
paramiko.util.log_to_file('paramiko.log')
class Mysql_connect2(object):
    def __init__(self,ip,type,c_user,c_pass=''):
        self.ip=ip
        self.real_ip=''
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())     
        self.c_user=c_user
        if (self.c_user=='root'):
            try:
                self.c_pass=r'byfLMurtD8E7O4xNmdznCsoYS3UJIq'
                self.ssh.connect(self.ip,22,self.c_user,self.c_pass,timeout=5)
            except:
                try:
                    self.c_pass=r'vef9oX$irzuxrfq_Wtkbqtabsj9djy'
                    self.ssh.connect(self.ip,22,self.c_user,self.c_pass,timeout=5)
                except:
                    try:
                        self.c_pass=r'byfLMurtD8E7O4xNmdznCsoYS3UJIq'
                        self.ssh.connect(self.ip,22,self.c_user,self.c_pass,timeout=5)
                    except:
                        try:
                            self.c_pass=r'zqStfilqbjnnxmoLqig4xgem6azs'
                            print self.c_pass
                            self.ssh.connect(self.ip,22,self.c_user,self.c_pass,timeout=5)
                        except:
                            try:
                                self.c_pass=r'Na4hycxdsk]hu0vkgnzig$x'
                                self.ssh.connect(self.ip,22,self.c_user,self.c_pass,timeout=5)
                            except:
                                self.c_pass=r'1qaz2wsx'
                                self.ssh.connect(self.ip,22,self.c_user,self.c_pass,timeout=5)
                        

        elif(self.c_user=='mysql'):
            try:
                self.c_pass=r'vef9oX$irzuxrfq_Wtkbqtabsj9djy'
                self.ssh.connect(self.ip,22,self.c_user,self.c_pass,timeout=5)
            except:
                try:
                    self.c_pass=r'byfLMurtD8E7O4xNmdznCsoYS3UJIq'
                    self.ssh.connect(self.ip,22,self.c_user,self.c_pass,timeout=5)
                except:
                    self.c_pass=r'dacri.k9qjxcew^d2sWJ_zmevt'
                    self.ssh.connect(self.ip,22,self.c_user,self.c_pass,timeout=5)
	else:
            try:
                self.c_pass=r'-zv>_0_z-84:_^u6fdsmTQ87a'
                self.ssh.connect(self.ip,22,self.c_user,self.c_pass,timeout=5)
            except:
                try:
                    self.c_pass=r'byfLMurtD8E7O4xNmdznCsoYS3UJIq'
                    self.ssh.connect(self.ip,22,self.c_user,self.c_pass,timeout=5)
                except:
                    self.c_pass=r'dacri.k9qjxcew^d2sWJ_zmevt'
                    self.ssh.connect(self.ip,22,self.c_user,self.c_pass,timeout=5)
         
        self.stdout=''
        self.out=''
        self.line=''
        self.type=type
        self.pager='>'
        self.db='mysql'
    def execute(self,m):
        self.stdin,self.stdout,self.stderr = self.ssh.exec_command("/sbin/ifconfig eth0 |grep 'inet addr' |awk '{print $2}' | awk -F ':' '{print $2}'")
        self.out=self.stdout.readlines()
        if (self.type=='mysql'):
            sock=m.split(":")[0]
            sql=m.split(":")[1]
            mysql_bin=m.split(':')[2]
            if  re.match('172.26.10',self.ip):
                m= mysql_bin+' -uroot  -S '+sock+' -p2Iwevjgbstbny<jmjjp6dvfD  '+self.db+' -e "'+sql+'"'
            else:
                m= mysql_bin+' -uroot  -S '+sock+' -pvsa#dxgqodaphk4bzky2sgrUq_Lyvb  '+self.db+" -e '"+sql+"'"
        self.stdin,self.stdout,self.stderr = self.ssh.exec_command(m)
        self.out=self.stdout.readlines()
        return self.out,self.stderr.readlines()
    def change(self,type_to):
        self.type=type_to 
    def print_info(self):
        if self.type=='os':
            print "========================"+self.ip+":"+self.type+self.pager
        elif self.type=='mysql':
            print "========================"+self.ip+":"+self.type+" db:"+self.db+self.pager
    def change_db(self,db):
        self.db=db.replace(";","")
        self.stdout=''
        self.out=''
        self.line=''
        self.type=type
        self.pager='>'
        self.db='mysql'
    def execute(self,m):
        self.stdin,self.stdout,self.stderr = self.ssh.exec_command("/sbin/ifconfig eth0 |grep 'inet addr' |awk '{print $2}' | awk -F ':' '{print $2}'")
        self.out=self.stdout.readlines()
        if (self.type=='mysql'):
            sock=m.split(":")[0]
            sql=m.split(":")[1]
            mysql_bin=m.split(':')[2]
            if  re.match('172.26.10',self.ip):
                m= mysql_bin+' -uroot  -S '+sock+' -p2Iwevjgbstbny<jmjjp6dvfD  '+self.db+' -e "'+sql+'"'
            else:
                #m= mysql_bin+' -uroot  -S '+sock+' -pjB6tCgI9fzEmPHS5R7e34csMbU8ZnO  '+self.db+' -e "'+sql+'"'
                m= mysql_bin+' -uroot  -S '+sock+' -pvsa#dxgqodaphk4bzky2sgrUq_Lyvb  '+self.db+' -e "'+sql+'"'
        self.stdin,self.stdout,self.stderr = self.ssh.exec_command(m)
        self.out=self.stdout.readlines()
        return self.out,self.stderr.readlines()
    def change(self,type_to):
        self.type=type_to 
    def print_info(self):
        if self.type=='os':
            print "========================"+self.ip+":"+self.type+self.pager
        elif self.type=='mysql':
            print "========================"+self.ip+":"+self.type+" db:"+self.db+self.pager
    def change_db(self,db):
        self.db=db.replace(";","")
