#-*- coding:utf-8 -*- 
import copy
import os
import sys
import MySQLdb
import MySQLdb.cursors
import time
import re
file_path=sys.path[0]
new_path=str(file_path)+"/mod/"
sys.path.append(new_path)
sys.path.append('/home/wangyunbo/class/')
from replication import *
from get_config_m import *
from scp_ssh_m import *
from  host_connect import *
import argparse
import ConfigParser
import pxssh

def get_basedir():
	dir_path=os.path.dirname(sys.argv[0])
	if len(dir_path)>=1:
		return dir_path
	else:
		return '.'
def cmd_ssh(ip,online,cmd):
        try:
		back_host=HostConnect(ip,'os','is_online','root')
		info,err_info=back_host.execute(cmd)
        	if (len(err_info)==0):
                	return "ok:"
        	else:
                	return "err:"
                	print err_info
	except:
		info=sys.exc_info()
		print (info[0],":",info[1])
		return 'err:'+str(info[0])+":"+str(info[1])
# Create your views here.
def  back_and_recover(master,slaves,nmaster,db_version,family_id,task_id):
	basedir=get_basedir()
	master_ip=master.split(':')[0]
	master_port=master.split(':')[1]
	new_master_ip_input=nmaster.split(':')[0]
  	new_master_port_input=nmaster.split(':')[1]
    	new_master_ip,new_master_port=get_master(master_ip,int(master_port))
	master_is_first=1
	status_list=[]
	version=get_verion(master_ip,master_port)
	if ((str((version.split('.')[0])+str(version.split('.')[1])))=='51'):
		ibback_path="/home/mysql/scripts/percona-xtrabackup-2.1/bin/xtrabackup"
	elif ((str((version.split('.')[0])+str(version.split('.')[1])))=='55'):	
		ibback_path="/home/mysql/scripts/percona-xtrabackup-2.1/bin/xtrabackup_55"
	elif ((str((version.split('.')[0])+str(version.split('.')[1])))=='56'):	
		ibback_path="/home/mysql/scripts/percona-xtrabackup-2.1/bin/xtrabackup_56"
	else:
		return "errr:the master version is not crreate,please check."
	conf_info={}
	conf_info['db_version']=db_version
	conf_info['os_root_online']=get_config('install','os_root_online')
	conf_info['mysql_path']=get_config('install','mysql_path')
	conf_info['remote_base_dir']=get_config('install','remote_base_dir')
	conf_info['center_ip']=get_config('install','center_ip')
	conf_info['backup']=get_config('install','backup')	
	conf_info['mysql_root']=get_config('install','mysql_root')
	#transf files 	
	remote_dir=conf_info['remote_base_dir']
	
	file_list=[basedir+"/soft/expect_create_rsa.sh",basedir+"/soft/create_idrsa.sh",basedir+"/soft/percona-xtrabackup-2.1.tar.gz",basedir+"/soft/perl-DBD-MySQL-4.013-3.el6.x86_64.rpm"]
	c_date=os.popen("date +%Y%m%d%H%M%s").readlines()[0].replace('\n','')
	cmd_mkdir_test="mkdir -p /usr/local/test"
	mkdir_log=cmd_ssh(master_ip,'online',cmd_mkdir_test)
	if (mkdir_log.split(":")[0]!="ok"):
		return "err:"+mkdir_log.replace('"','').replace("'",'')
	info=scp_cmd(master_ip,file_list,'root',conf_info['os_root_online'],remote_dir)
	if (info=='ok'):
		master_host=HostConnect(master_ip,'os','is_online','root')
                info,err_info=master_host.execute('yum -y install perl-DBD-MySQL')
                if (len(err_info)>=1):
			print err_info
			#return "err: "+master_ip+" install perl-DBD-MySQL err"
		info,err_info=master_host.execute('yum -y install perl-Time-HiRes')
                if (len(err_info)>=1):
			print err_info
                	#return "err: "+master_ip+" yum -y install perl-Time-HiRes"
                info,err_info=master_host.execute('tar -zxf /usr/local/test/percona-xtrabackup-2.1.tar.gz  -C  /home/mysql/scripts/')
                if (len(err_info)>=1):
			return "err:"+master_ip+"tar -zxf /usr/local/test/percona-xtrabackup-2.1.tar.gz  -C  /home/mysql/scripts/"
		info,err_info=master_host.execute('which expect')
		print info,err_info
		if (len(err_info)>=1):
			if re.search('no expect',err_info[0]):
				master_host.execute('yum -y install expect')
			else:
			
				return "err:no expect ,please instal first "+master_ip
		find_defaults_file="ps -ef | grep 'mysqld --' | grep  port='"+str(master_port)+"' |awk '{print $9}' | awk -F'='   '{print $2}'"
		print find_defaults_file
		info,err_info=master_host.execute(find_defaults_file)
		if (len(info)>=1):
			defaults_file_m=info[0].replace('\n','')
			if re.search('cnf',defaults_file_m):
				print 'ok'
			else:
				defaults_file_m='/export/servers/mysql/etc/my.cnf'
		else:
			defaults_file_m='/export/servers/mysql/etc/my.cnf'
			print "err:find defaults-file err"+master_ip
			return "err:find defaults-fle err "+master_ip
		get_datadir="cat "+defaults_file_m+" | grep innodb_data_home_dir | awk -F'=' '{print $2}'"
		print get_datadir
		info,err_info=master_host.execute(get_datadir)
		print info
		if (len(info)>=1):
			datadir_l=info[0].replace('\n','').replace(' ','').split('/')
			datadir_m=''
			for i  in range(0,len(datadir_l)-1):
				datadir_m=datadir_m+str(datadir_l[i])+"/"
			print datadir_m
		else:
			print "err:find defaults-file err"+master_ip
			return "err:find defaults-fle err "+master_ip
	
		print '111111111111111111111111111111111111111111111'
		info,err_info=master_host.execute('which expect')
		print info,err_info
		if (len(err_info)>=1):
			print "err:the master has no expect ,please install"+master_ip
			return "err:the master has no expect ,please install"+master_ip
		else:
			err_list_info=[]
			for slave in slaves.split(";"):
				slave_ip=slave.split(':')[0]
				slave_port=slave.split(':')[1]
				
				slave_host=HostConnect(slave_ip,'os','is_online','root')
				slave_host.execute('mkdir -p /root/.ssh')
				slave_host.execute('chmod 555 /root/.ssh')
				install_idrsa="/usr/local/test/create_idrsa.sh  "+slave_ip+" root"
				info,err_info=master_host.execute(install_idrsa)
				err_info=[]
				if (len(err_info)>=1):
					print err_info
					err_line="err:"+master_ip+" create idrsa to "+slave_ip
					print err_line
					err_list_info.append(err_line)
					break
				else:
					
					slave_host=HostConnect(slave_ip,'os','is_online','root')
					find_defaults_file="ps -ef | grep 'mysqld --' | grep  port='"+str(slave_port)+"' |awk '{print $9}' | awk -F'='   '{print $2}'"
					print find_defaults_file
					info,err_info=slave_host.execute(find_defaults_file)
					print err_info
					if (len(info)>=1):
						defaults_file_s=info[0].replace('\n','')
					else:
						defaults_file_s='/export/servers/mysql/etc/my.cnf'
						line="err:find defaults-file err"+slave_ip
						print line
					get_datadir="cat "+defaults_file_s+" | grep innodb_data_home_dir | awk -F'=' '{print $2}'"
					info,err_info=slave_host.execute(get_datadir)
					if (len(info[0])>=1):
						datadir_l=info[0].replace('\n','').replace(' ','').split('/')
						datadir_s=''
						for i  in range(0,len(datadir_l)-1):
							datadir_s=datadir_s+str(datadir_l[i])+"/"
						print datadir_s+"---------------"
					else:
						line="err:find defaults-file err"+slave_ip
						err_list_info.append(line)
						break
				
					
					#get_baseder                            
                                        get_mysqlbasedir="ps -ef | grep 'mysqld' | grep  port='"+str(slave_port)+"' | grep -v 'grep' |awk '{print $8}' "
                                        info,err_info=slave_host.execute(get_mysqlbasedir)
                                        if (len(err_info)==0):
                                                mysql_basedir=info[0].replace('\n','').replace(' ','')
                                                mysqld_safe_path=mysql_basedir.replace('mysqld','mysqld_safe')
                                                mysqld_admin_path=mysql_basedir.replace('mysqld','mysqladmin')
                                        else:
                                                line="err:find defaults-file err"+slave_ip
                                                err_list_info.append(line)
                                                break
                                        print mysqld_safe_path
	
					cmd_mkdir_test="mkdir -p /usr/local/test"
					mkdir_log=cmd_ssh(slave_ip,'online',cmd_mkdir_test)
					if (mkdir_log.split(":")[0]!="ok"):
						return "err:"+mkdir_log.replace('"','').replace("'",'')+" "+slave_ip
					
					info=scp_cmd(slave_ip,file_list,'root',conf_info['os_root_online'],remote_dir)
					if (info=='ok'):
                				info,err_info=slave_host.execute('yum -y install perl-DBD-MySQL')
                				if (len(err_info)>=1):
							print err_info
							print   "err: "+slave_ip+" install per-DBD-MySQL err"
								
						info,err_info=slave_host.execute('yum -y install perl-Time-HiRes')
                				if (len(err_info)>=1):
							print err_info
                					print "err: "+slave_ip+" yum -y install perl-Time-HiRes"
                				info,err_info=slave_host.execute('tar -zxf /usr/local/test/percona-xtrabackup-2.1.tar.gz  -C  /home/mysql/scripts/')
                				if (len(err_info)>=1):
							return "err:"+slave_ip+"tar -zxf /usr/local/test/percona-xtrabackup-2.1.tar.gz  -C  /home/mysql/scripts/"
					else:
						return  "err:scp to "+str(slave_ip)+"err,please check root password"
					
					backup_dir=datadir_s+""+c_date	
					cmd_mkdir_backup="mkdir -p "+datadir_s+""+c_date
					print cmd_mkdir_backup
					mkdir_log=cmd_ssh(slave_ip,'online',cmd_mkdir_backup)
					if (mkdir_log.split(":")[0]!="ok"):
						line="err:"+mkdir_log.replace('"','').replace("'",'')
						err_list_info.append(line)
						break		
					xtrab_back="nohup /home/mysql/scripts/percona-xtrabackup-2.1/bin/innobackupex  --ibbackup="+ibback_path+"  --defaults-file="+defaults_file_m+"  --slave-info  --user=backup  --password="+conf_info['backup']+"   --stream=tar  "+datadir_s+" 2> /var/log/"+c_date+".log  | gzip -1  | ssh root@"+slave_ip+" cat \">\"   "+backup_dir+"/xtr.tar.gz 2>&1 >/dev/null &"
					print xtrab_back
					master_host.execute(xtrab_back)
					find_log="cat /var/log/"+c_date+".log | grep 'innobackupex: completed OK!'"
					info,err_info=master_host.execute(find_log)
					print find_log
					try:
						end_message=info[0]
					except:
						end_message=''
					if re.search('innobackupex: completed OK!',end_message):
						unzip_file="nohup tar -izxf "+backup_dir+"/xtr.tar.gz -C "+backup_dir +"&"
						xtrab_recover="nohup /home/mysql/scripts/percona-xtrabackup-2.1/bin/innobackupex --apply-log  --ibbackup="+ibback_path+"  "+backup_dir +" > /var/log/"+c_date+".log 2>&1 >/dev/null "
						
						rm_xtr_file="/bin/rm -rf "+backup_dir+"/xtr.tar.gz"
						print unzip_file
						info,err_info=slave_host.execute(unzip_file)
						print err_info,info
						print xtrab_recover
						info,err_info=slave_host.execute(rm_xtr_file)
						print time.time(),'start recover'	
						slave_host.execute(xtrab_recover)
						print time.time(),'end recover'	
						print err_info,info
						time.sleep(50)
						find_log="cat /var/log/"+c_date+".log | grep 'innobackupex: completed OK!'"
						info,err_info=slave_host.execute(find_log)
						print info
						end_message=info[0]
						if re.search('innobackupex: completed OK!',end_message):
							print "recover ok"
							get_ibdat_conf="cat "+backup_dir+"/backup-my.cnf  | grep  innodb_data_file_path"
							info,err_info=slave_host.execute(get_ibdat_conf)
							if (len(err_info)==0):
								ibdat_conf=info[0].replace("\n",'')
							else:
								return "err:"+slave_ip+"get_ibdat_conf err"
							replace_ibdat="sed -i 's/innodb_data_file_path.*/"+ibdat_conf+"/g' "+defaults_file_s
											
							info,err_info=slave_host.execute(replace_ibdat)
							if (len(err_info)==0):
								print "replace_ibdat"+slave_ip
							else:
								return "err:"+slave_ip+"replace_ibdat  err"
	
							get_log_file_groups="cat "+backup_dir+"/backup-my.cnf  | grep  innodb_log_files_in_group"
							info,err_info=slave_host.execute(get_log_file_groups)
							if (len(err_info)==0):
								log_file_groups=info[0].replace("\n",'')
							else:
								return "err:"+slave_ip+"get_log_file_groups err"
							replace_log_groups="sed -i 's/innodb_log_files_in_group.*/"+log_file_groups+"/g' "+defaults_file_s
							print replace_log_groups
							
							info,err_info=slave_host.execute(replace_log_groups)
							if (len(err_info)>=1):
								print err_info[0]+" "+replace_log_groups
								return "err:"+replace_log_groups
							
							get_log_file_size="cat "+backup_dir+"/backup-my.cnf  | grep  innodb_log_file_size"
							info,err_info=slave_host.execute(get_log_file_size)
							if (len(err_info)==0):
								log_file_size=info[0].replace("\n",'')
							else:
								return "err:"+slave_ip+"get_log_file_size err"
							replace_log_file_size="sed -i 's/innodb_log_file_size.*/"+log_file_size+"/g' "+defaults_file_s
							
							info,err_info=slave_host.execute(replace_log_file_size)
							if (len(err_info)>=1):
								print err_info[0]+" "+replace_log_file_size
								return "err:"+replace_log_file_size
							print replace_log_file_size
							rep_grant_log=replication_grant(master_ip,master_port,slave_ip)
							if (rep_grant_log!='ok'):
								print rep_grant_log
								print 'err:add replication users err,@'+master_ip
								return 'err:add replication users err,@'+master_ip
							
							stop_mysql=mysqld_admin_path+" -uroot -p"+str(conf_info['mysql_root'])+" shutdown"
                                                        print stop_mysql
							
							
							info,err_info=slave_host.execute(stop_mysql)
							if (len(err_info)>=1):
								print err_info[0]+" "+stop_mysql
								return "err:"+stop_mysql
				
                                                        #back_datadir="mv " +datadir_s+"data "+datadir_s+"data_back"+str(c_date)
                                                        
                                                        back_datadir="cd "+datadir_s+"  && tar  -zcvf  "+str(c_date)+".tar.gz  data "
							print back_datadir
							info,err_info=slave_host.execute(back_datadir)
							if (len(err_info)>=1):
								print err_info[0]+" "+back_datadir
								return "err:"+back_datadir
							
                                                        rm_datadir="/bin/rm -rf  "+datadir_s+"data/* "
							print rm_datadir
							info,err_info=slave_host.execute(rm_datadir)
							if (len(err_info)>=1):
								print err_info[0]+" "+rm_datadir
								return "err:"+rm_datadir
							
                                                        recover_datadir="mv "+backup_dir+"/*  "+datadir_s+"data"
                                                        print recover_datadir
							info,err_info=slave_host.execute(recover_datadir)
							if (len(err_info)>=1):
								print err_info[0]+" "+recover_datadir
								return "err:"+recover_datadir
                                                        chown_own="chown -R mysql.mysql   "+datadir_s+"data "
                                                        print chown_own
							info,err_info=slave_host.execute(chown_own)
							if (len(err_info)>=1):
								print err_info[0]+" "+chown_own
								return "err:"+chown_own
                                                        start_mysql="nohup "+mysqld_safe_path+"  --defaults-file="+defaults_file_s+"  --user=mysql > /dev/null 2>&1 & "
                                                        print start_mysql
							info,err_info=slave_host.execute(start_mysql)
							if (len(err_info)>=1):
								print err_info[0]+" "+start_mysql
								return "err:"+start_mysql
							time.sleep(20)	
							if (master_ip==new_master_ip_input):
								get_master_info="cat "+datadir_s+"data/xtrabackup_binlog_info"
								info,err_info=slave_host.execute(get_master_info)
								if (len(err_info)>=1):
									print err_info[0]+" "+get_master_info
									return "err:"+get_master_info
								else:
									master_log_file=info[0].split('\t')[0].replace(' ','')
									master_log_pos=info[0].split('\t')[1].replace(' ','')
									print master_log_file,master_log_pos
								change_master_log=change_master(master_ip,master_port,master_log_file,master_log_pos,slave_ip,slave_port)
							else:
								get_master_info="cat "+datadir_s+"data/xtrabackup_slave_info"
								print get_master_info
								info,err_info=slave_host.execute(get_master_info)
								print info,'info'
								print err_info,'err_info'
								if (len(err_info)>=1):
									print err_info[0]+" "+get_master_info
									return "err:"+get_master_info
								else:
									print info
									master_log_file=info[0].split('=')[1].split(',')[0].replace("'","")
									master_log_pos=info[0].split('=')[2].replace(' ','')
									print master_log_file,master_log_pos
								change_master_log=change_master(new_master_ip,new_master_port,master_log_file,master_log_pos,slave_ip,slave_port)
							if (change_master_log=='ok'):
								start_slave_log=start_slave(slave_ip,slave_port)
								if (start_slave_log=='ok'):
									time.sleep(10)
									master_host.execute('/bin/rm -rf    /root/.ssh/authorized_keys')
									check_slave_log=check_slave(slave_ip,slave_port)
									print check_slave_log,'check_slave_log'
									return "ok"
								else:
									return 'err:start slave err'
							
							else:
								print change_master_log
								return slave_ip+"change_master_ err"
							#	print change_master_log
							#	print 'err:add replication users err,@'+master_ip
							#	return 'err:add replication users err,@'+master_ip
						else:
							print ''
							return 'err:recover err'
					else:
						print 'err:backup err'
						return  'err:backup err '
	else:
		#status_list.addppend('err')
		print "update log"
		return  "err:scp to "+str(master_ip)+"err,please check root password"
def write_input_conf(conf_dict):
	basedir=get_basedir()	
	host_ip=conf_dict['op_ip']
	db_version=conf_dict['db_version']	
	input_tmp_file_name=basedir+"/install_files/"+db_version+"/input_"+host_ip+".conf"
        input_tmp_file = open(input_tmp_file_name, "w")
	keys=conf_dict.keys()
	keys.sort()
	for  key in keys:
		line=key+"="+str(conf_dict[key])+"\n"
		input_tmp_file.write(line)
	input_tmp_file.close()

def argparser():
        parser = argparse.ArgumentParser(description='MySQL xtrabback and recover tools')
        parser.add_argument('-f',dest='from',default='',help='ip:port')
        parser.add_argument('-t',dest='to',default='',help='ip:port')
        parser.add_argument('-m',dest='master',default='',help='ip:port')
        parser.add_argument('-a',dest='family_id',type=int,help='family_id  in Dbs table.')
        parser.add_argument('-s',dest='task_id',type=int,help='task id in Task table.')
        parser.add_argument('-r',dest='role',default='',help='role to mysqlmgrsys.')
	args = parser.parse_args()
        return vars(args)
if __name__ == "__main__":
    args=argparser()
    from_host=args['from']
    to_hosts=args['to']
    master=args['master']
    family_id=args['family_id']
    task_id=args['task_id']
    role=args['role']
    print role
    end_status=[]
    time.sleep(5)
    info=mysql_check_env(from_host,to_hosts,master)
    if (info.split(":")[0]=='ok'):
        sql="update machines_replicationsetup  set check_envok=1,check_envmessage='ok' where id="+str(task_id)
        sql=update_center_info(sql)
    else:
        sql="update machines_replicationsetup  set check_envok=0,check_envmessage='"+info+"' where id="+str(task_id)
        sql=update_center_info(sql)
        sys.exit(0)
    print sql
    #暂停监控
    to_ip=to_hosts.split(":")[0]
    to_port=to_hosts.split(":")[1]
    from_ip=from_host.split(":")[0]
    from_port=from_host.split(":")[1]
    update_zabbix_info(to_ip,to_port,'disable')
    
    #判断当前进行的任务数
    get_task_count_sql="select count(*)  as num from    machines_replicationsetup  where rep_message='running'"
    task_num=update_center_info(get_task_count_sql)
    while (int(task_num[0]['num'])>=10):
        time.sleep(60)
        task_num=update_center_info(get_task_count_sql)
    #查看前置任务 
    get_before_count_sql="select count(*) as num from  machines_replicationsetup   where (master_ip='"+from_host+"' or new_master like  '"+from_host+"%' )  and rep_ok!=1 and id<"+str(task_id)
    before_task=update_center_info(get_before_count_sql)
    print before_task
    while ( len(before_task)>=1 and   int(before_task[0]['num'])>=1):
        time.sleep(58)
        print from_ip," has before task"
        print get_before_count_sql
        before_task=update_center_info(get_before_count_sql)
    sql="update machines_replicationsetup  set rep_message='running' where id="+str(task_id)
    update_center_info(sql)
    to_ip=to_hosts.split(":")[0]
    to_port=to_hosts.split(":")[1]
    from_ip=from_host.split(":")[0]
    from_port=from_host.split(":")[1]
    update_zabbix_info(to_ip,to_port,'disable')
    end_status=back_and_recover(from_host,to_hosts,master,'mysql5.5.14',family_id,task_id)
    print end_status
    if (end_status=="ok"):	
        sql="update machines_replicationsetup  set rep_ok=1,rep_message='ok', finished=1 where id="+str(task_id)
        print sql
        update_center_info(sql)
        update_zabbix_info(to_ip,to_port,'enable')
        if (role!='no'):
            a=update_mgr_info(from_ip,to_ip,role,from_port)
            print a
    else:
        sql="update machines_replicationsetup  set rep_ok=0,rep_message='"+str(end_status)+"' where id="+str(task_id)
        print sql
        update_center_info(sql)
        #update_zabbix_info(to_ip,to_port,'enable')
