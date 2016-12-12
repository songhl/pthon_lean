#coding:utf8
#author:xyk(xgtiger@163.com)
#分割mysqldump导出的文件,可以按数据库名称或表名称截取需要的内容。
#2014.4.29  all test ok
#2014.5.29  bug tb_start
#2014.6.23  去除-F
import sys,re,os
reload(sys)
sys.setdefaultencoding('utf8')
def start_proc(cmd,output=False,getoutput=True):
    import subprocess
    process = subprocess.Popen(cmd,shell = True, stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
    if getoutput:
        out,err=process.communicate(None)
        return (process.returncode,out)
    if output:
        while True:
            line = process.stdout.readline()
            if not line:
                break
            print('out-->' + line.strip())
        print('out-->DONE')
    retcode=process.wait()
    if retcode==0:
        return 0
    else:
        return 1

def cancel(aa,bb):
    print u'\n已取消'
    sys.exit(1)
    
class CutDumpedSql():
    
    def __init__(self):
        import signal
        signal.signal(signal.SIGTERM, cancel)
        signal.signal(signal.SIGINT, cancel)
    
    
    def __show_view_info(self,database,list_view=None,ignore_case=False):    
        if self.dict_db_view.has_key(database):
            print 
            view_start=self.dict_db_view[database][0]
            view_end=self.dict_db_view[database][1]
            dict_view=self.dict_db_view[database][2]
            if len(dict_view)==0:
                if list_view is not None:
                    print u"\033[31m注意：注意：存在未能被找到的视图:"
                    print "\n".join([val for val in list_view if val not in dict_view.keys()])
                    print "\n\033[0m"
            else:
                print u'\033[32mView Info:'
                if list_view is None:
                    print u'start: %-10s'%str(view_start)+u'end: %-10s'%str(view_end)+'\033[0m\n'
                    keys=dict_view.keys()
                else:#或许要区分大小写
                    if ignore_case:
                        dict_case_view={}
                        for view in dict_view:
                            dict_case_view[view.lower()]=view
                        keys=[]
                        for v in list_view:
                            if v.lower() in dict_case_view:
                                keys.append(dict_case_view[v.lower()])
                    else:
                        keys=[val for val in list_view if val in dict_view.keys()]
                keys.sort()
                for view in keys:
                    print '\033[33mView  %-32s'%view+'start: %-10s'%str(dict_view[view]['start'])+'end: %-10s'%str(dict_view[view]['end'])+'\033[0m'
                if list_view is not None and len(keys)!=len(list_view):
                    if ignore_case:
                        print u"\033[31m注意：存在即使忽略大小写，仍未能被找到的视图："
                        
                        dict_view_case=self.dict_case_sense[database.lower()][2]
                        print "\n".join([val for val in list_view if val.lower() not in dict_view_case.keys()])
                        print "\033[0m"
                    else:
                        print u"\033[31m注意：注意：存在未能被找到的视图(试试--ignore-case):"
                        print "\n".join([val for val in list_view if val not in dict_view.keys()])
    
    def check(self,filename,is_print):
        
        '''1.get boundry of database and table
        2.print summury of the sql file,if is_print is true.'''
        #{test:[1, 3379,{'audit_repayment': {'start': 7130, 'end': 7172}, 'oauth_qq': {'start': 1614, 'end': 1657}  } ] ,   ,  ,  }
        #cmd=r"sed -n -e '/-- Current Database: `\(.*\)`/I{=;p}' -e '/-- Table structure for table `\(.*\)`/I{=;p}' %s | sed -n '/^[0-9]*$/{N;s/\n/:/p}'|sed -n 's/--.*`\(.*\)`/\1/p'"%(filename)
        cmd=r"sed -n -e '/^-- Current Database: `\(.*\)`/{=;p}' -e '/^-- Table structure for table `\(.*\)`/{=;p}' -e '/^-- Final view structure for view `\(.*\)`/{=;p}' -e '${=;s/.*/lastline/;p}' %s | sed -n '/^[0-9]*$/{N;s/\n/:/p}' "%(filename)
        
                            

                    
        begin_nums=start_proc(cmd)[1].split('\n')
        
        cur_db='';self.dict_db={};dict_tb={};dict_view={};  db_start=None;db_end=None;
        self.dict_db_view={};self.dump_msg_num=None;vw_start=None;vw_end=None;dump_msg_found=False
        
        for i,v in enumerate(begin_nums):
            if re.match('.*Current Database: `.*',v,re.I):
                
                if dump_msg_found is False: #第一次找到起始信息
                    cur_db=re.search("`(?P<bbb>.*)`",v).group("bbb")
                    db_start=int(v.split(":")[0])
                    self.dump_msg_num=int( db_start )-1
                    dump_msg_found=True
                else:
                    new_db_start=int(v.split(":")[0])
                    new_cur_db=re.search("`(?P<bbb>.*)`",v).group("bbb")
                    db_end=new_db_start-1
                    if not self.dict_db.has_key(cur_db):#database data
                        self.dict_db[cur_db]=[db_start,db_end,dict_tb]
                        dict_tb={}
                        
                    else:#database  view
                        self.dict_db_view[cur_db]=[db_start,db_end,dict_view]
                        dict_view={}
                    
                    cur_db=new_cur_db
                    db_start=new_db_start
                        
            if re.match('.*Table structure for table `.*',v,re.I):
                cur_tb=re.search("`(?P<bbb>.*)`",v).group("bbb")
                tb_start=v.split(':')[0]
                tb_end=int(begin_nums[i+1].split(":")[0]) - 1
                dict_tb[cur_tb]={"start":int(tb_start.strip()),"end":tb_end}
                if db_start is None:#无DB NAME，从第一个table开始计数
                    db_start=tb_start
                    self.dump_msg_num=int(db_start)-1
                
            if re.match('.*Final view structure for view `.*',v,re.I):
                cur_view=re.search("`(?P<bbb>.*)`",v).group("bbb")
                vw_start=int(v.split(':')[0].strip())
                vw_end=int(begin_nums[i+1].split(":")[0].strip()) - 1
                dict_view[cur_view]={"start":vw_start,"end":vw_end}
                
            if re.match('\d+:lastline',v):
                if dict_view!={}:#存在的视图
                    list_view=dict_view.keys()
                    list_view.sort()
                    db_vw_start=db_start#int(dict_view[list_view[0]]['start'])
                    db_end= db_vw_start - 1
                    db_vw_end=int(v.split(":")[0])
                else:
                    db_end=int(v.split(":")[0])
                    db_vw_start=db_vw_end=db_end
                    
                
                if not self.dict_db_view.has_key(cur_db):
                    self.dict_db_view[cur_db]=[db_vw_start,db_vw_end,dict_view]
                if not self.dict_db.has_key(cur_db):
                    self.dict_db[cur_db]=[db_start,db_end,dict_tb]
                
        
        if is_print:
            pass
            if len(self.dict_db)==0:
                print '\033[32mNo database found !\033[0m'
            else:
                keys=self.dict_db.keys()
                keys.sort()
                for db in keys:

                    db_start=self.dict_db[db][0]
                    db_end=self.dict_db[db][1]
                    print '\033[34m\n$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$\033[0m'
                    if db=='':
                        name=filename
                    else:
                        name=db
                    print u'\033[32mDatabase  %-20s '%name
                    print u'start: %-10s'%str(db_start)+u'end: %-10s'%str(db_end)+'\033[0m'
                    print 
                    
                    dict_table=self.dict_db[db][2]
                    if len(dict_table)==0:
                        print u'\033[31m在%s库没发现任何表！\033[0m'%db
                    else:
                        keys=dict_table.keys()
                        keys.sort()
                        for tb in keys:
                            print '\033[36mTable %-32s'%tb+'start: %-10s'%str(dict_table[tb]['start'])+'end: %-10s'%str(dict_table[tb]['end'])+'\033[0m'
                    self.__show_view_info(db)
                


    def cut(self,filename,list_database,list_table,list_view,ignore_case):
        u'''分割mysqldump导出的文件，list_database指明需要操作的所有数据名称；只有一个数据库指明时，可以截取其中的某些表，使用list_table；ignore_case指明库名或表名是否大小写敏感。
        '''
        
        if len(list_database)==0:
            print '\033[31mNo database specified!!\033[0m'
            sys.exit(1)
        self.check(filename, is_print=False)
        
        if ignore_case :
            self.dict_case_sense={}
            for db in self.dict_db.keys():
                list_tb=self.dict_db[db][2].keys()
                if self.dict_db_view.has_key(db):##################################add has_key
                    list_vw=self.dict_db_view[db][2]
                else:
                    list_vw=[]
                dict_tb_case={}
                for tb in list_tb:
                    dict_tb_case[tb.lower()]=tb   
                dict_view_case={}
                for view in list_vw:
                    dict_view_case[view.lower()]=view
                self.dict_case_sense[db.lower()]=(db,dict_tb_case,dict_view_case) 
        if len(list_database)==1:
            if ignore_case :
                pass
            elif list_database[0] not in self.dict_db.keys() and '' not in self.dict_db.keys():
                print u'\033[31m没找到%s库，如果它的确存在，试试"--ignore-case"\033[0m'%(list_database[0])
                sys.exit(1)
            database_pri=list_database[0]

            
            if ignore_case and database_pri.lower() in self.dict_case_sense.keys():
                database=self.dict_case_sense[database_pri.lower()][0]
                
            elif database_pri  in self.dict_db.keys() :
                database=database_pri
            elif '' in self.dict_db.keys():
                database=""
            else:
                database=None
            if database is None:
                print u'\033[31m没找到%s库，即使不区分大小写。\033[0m'%(list_database[0])
                sys.exit(1)
            else:
                #cmd for table
                dict_table=self.dict_db[database][2]
                cmd_l='';
                if self.dump_msg_num is not None:
                    cmd_l+=" -e '%d,%dp' "%(1,self.dump_msg_num)
                if database=="":
                    outfile=filename
                else:
                    outfile=database
                
                if list_table is None:#one whole database
                    database_begin_num=self.dict_db[database][0]
                    database_end_num=self.dict_db[database][1]
                    cmd="sed -n -e '%s,%sp' "%(database_begin_num,database_end_num)+cmd_l+" ### %s > %s.cut"%(filename,outfile)
                    list_table=dict_table.keys()
                    list_table.sort()
                    tb_list_sum=list_table
                    

                else:#table  list  of  one database
                    tb_list_sum=[]
                    list_table.sort()
                    if ignore_case:
                        dict_tb_case=self.dict_case_sense[database.lower()][1]
                    for tb in list_table:
                        if ignore_case and tb.lower() in dict_tb_case.keys():
                            key=dict_tb_case[tb.lower()]
                        elif dict_table.has_key(tb)  :
                            key=tb
                        else:
                            key=None
                        if key is not None:
                            tb_list_sum.append(key)
                            table_begin_num=dict_table[key]['start']
                            table_end_num=dict_table[key]['end']
                            cmd_l+=" -e '%d,%dp' "%(table_begin_num,table_end_num)
                    cmd="sed -n "+cmd_l+" ### %s > %s.cut"%(filename,outfile)
                #cmd for view
                cmd_ll=''
                if self.dict_db_view.has_key(database):
                    dict_view=self.dict_db_view[database][2]
                    if list_view is None:
                        if list_table is None:#完整的单库
                            view_start=self.dict_db_view[database][0]
                            view_end=self.dict_db_view[database][1]
                            dict_view=self.dict_db_view[database][2]
                            cmd_ll=" -e '%d,%dp' "%(int(view_start),view_end)
                        else:
                            pass#不指明整个库，并且不指明视图列表时，默认不截取视图！！！
                        
                    else:#view list
                
                        view_list_sum=[]
                        list_view.sort()
                        if ignore_case:
                            dict_view_case=self.dict_case_sense[database.lower()][2]
                        for view in list_view:
                            if ignore_case and view.lower() in dict_view_case.keys():
                                key=dict_view_case[view.lower()]
                            elif dict_view.has_key(view)  :
                                key=view
                            else:
                                key=None
                            if key is not None:
                                view_list_sum.append(key)
                                view_begin_num=dict_view[key]['start']
                                view_end_num=dict_view[key]['end']
                                cmd_ll+=" -e '%d,%dp' "%(view_begin_num,view_end_num)
                cmd=cmd.replace("###", cmd_ll)
                
                
                if len(tb_list_sum) ==0:
                    if dict_table=={}:
                        
                        print u'\033[31m%s库中不存在表！\033[0m'%database
                    else:
                        if ignore_case:
                            print u'\033[31m注意：存在即使忽略大小写，仍未能被找到的表:'
                            dict_tb_case=self.dict_case_sense[database.lower()][1]
                            print "\n".join([val for val in list_table if val.lower() not in dict_tb_case.keys()])
                        else:
                            print u'\033[31m在%s库中没找到符合要求的表,或许可以试试--ignore-case\033[0m'%database
                    
                    sys.exit(1)
                else:
                    #table
                    print u'\033[32m%s库中找到%d张满足要求的表:\033[0m'%(database,len(tb_list_sum))
                    print "\033[36m"
                    print "\n".join([val for val in tb_list_sum])
                    print '\n\033[0m'
                    
                    
                    if list_table and len(tb_list_sum)!=len(list_table):
                        if ignore_case:
                            print u'\033[31m注意：存在即使忽略大小写，仍未能被找到的表:'
                            dict_tb_case=self.dict_case_sense[database.lower()][1]
                            print "\n".join([val for val in list_table if val.lower() not in dict_tb_case.keys()])
                            
                        else:
                            print u'\033[31m注意：存在未能被找到的表(试试--ignore-case):'
                            print "\n".join([val for val in list_table if val not in dict_table.keys()])
                        print '\033[0m'
                    
                    #view
                    if list_view is not None:
                        
                        self.__show_view_info(database,list_view,ignore_case=ignore_case)
                    
                    if raw_input('\nstart?（Y/n）') in ('Y' ,'y'):
                        print [cmd]
                        ret=start_proc(cmd)
                        if ret[0]  == 0:
                            print u'\033[32m截取成功：已保存到文件%s.cut\n %s：%s \n\nall_success!\033[0m'%(outfile,database_pri,','.join(tb_list_sum))
                        else:
                            print u'\033[31m不能生成新文件 %s.cut !\033[0m'%outfile
                            sys.exit(1)
                    else:
                        print u'已取消.'
                        sys.exit(1)
        else:#many databases
            
            if ignore_case :
                m=[val for val in list_database if val.lower() not in self.dict_case_sense.keys()]
                if len(m)!=0 :
                    print u'\033[31m即使忽略大小写，仍没找到%s库\033[0m'%(','.join(m))
                    sys.exit(1)
                else:
                    list_database_new=[self.dict_case_sense[db.lower()][0] for db in list_database]
            else:
                i=[val for val in list_database if val not in self.dict_db.keys()]
                if   len(i)!=0:
                    print u'\033[31m没找到%s库，如果它的确存在，试试"--ignore-case"\033[0m'%(','.join(i))
                    sys.exit(1)
                else:
                    list_database_new=list_database
            list_database_new.sort()
            
            cmd_l='';cmd_ll=""
            if self.dump_msg_num is not None:
                cmd_l+=" -e '%d,%dp' "%(1,self.dump_msg_num)
                
            for db in list_database_new:
                if self.dict_db.has_key(db):
                    #data
                    start=int(self.dict_db[db][0])
                    end=int(self.dict_db[db][1])
                    cmd_l+=" -e '%d,%dp' "%(start,end)
                    #view
                    if self.dict_db_view.has_key(db):
                        view_start=self.dict_db_view[db][0]
                        view_end=self.dict_db_view[db][1]
                        cmd_ll+=" -e '%d,%dp'"%(int(view_start),int(view_end))
                else:
                    print u'没找到库%s'%db,'this should not happen'
            cmd="sed -n "+cmd_l+" ### %s > %s.cut"%(filename,filename)
            
            
            # cmd for view
            cmd=cmd.replace('###',cmd_ll)
            if list_table is not None and list_view is not None:
                print u'\033[33m当有多个DB被指明时，--tables(-t)和--views(-v)选项已被忽略！！\033[0m'
            elif list_table is not None:
                print u'\033[33m当有多个DB被指明时，--tables(-t)选项已被忽略！！\033[0m'
            elif list_view is not None:
                print u'\033[33m当有多个DB被指明时，--views(-v)选项已被忽略！！\033[0m'
            
            print u'\033[32m找到符合要求的DB:'
            print "\n".join([val for val in list_database_new])
            print '\n\033[0m'
            
            p=raw_input('\nstart?（Y/n）')
            
            if p=='Y' or p=='y':
                ret=start_proc(cmd)
                if ret[0]  == 0:
                    print u'\033[32m截取成功: 已保存到文件%s.cut\n %s \n\nall_success!\033[0m'%(filename,','.join(list_database_new))
                else:
                    print u'\033[31m不能生成新文件 %s.cut !\033[0m'%filename
                    sys.exit(1)
            else:
                print u'已取消.'

            
        
        
    def get_parser(self):
        from optparse import OptionParser
        parser = OptionParser()
#        parser.add_option("-f","--sql-file",action='store', type='string', dest="filename",
#                          metavar='sql-file',default=None,
#                          help=
#                          u'''指明标准的用mysqldump导出的sql文件。   ''')
        
        parser.add_option("-B","--databases",action='store', type='string',dest="databases",
                          help=
                          u'''指明需要操作的所有数据名称，至少指明一个；可以是多个（用英文逗号分隔）,此时--tables被忽略；只有一个数据库指明时，可以截取其中的某些表，使用--tables。''')
        
        parser.add_option("-t","--tables",action='store', type='string',dest="tables",
                          help=
                          u'''指明要截取的表，可以是多个（用英文逗号分隔），默认是所选DB的所有表。''')
        
        parser.add_option("-v","--views",action='store', type='string',dest="views",
                          help=
                          u'''指明要截取的视图，可以是多个（用英文逗号分隔），默认是所选DB的所有视图。''')
        
        parser.add_option("-i","--ignore-case",action='store_true', dest="ignore",default=False,
                          help=
                          u'''DATABASE和TABLE名称是否忽略大小写（忽略大小写会降低查找效率），默认不忽略。''')
        parser.add_option("-c","--check",action='store_true', dest="check",default=False,
                          help=
                          u'''仅显示sql文件中的库和表信息。''')
        return parser
        
    def work(self):
        parser=self.get_parser()
        (options, args) = parser.parse_args()
        if args:
            filename=args[0]
        else:
            filename=''
        if options.check  and filename:
            self.check(filename=filename, is_print=True)
        elif filename and options.databases:
            try:
                list_tables=None;list_views=None
                list_database=options.databases.split(',')
                if options.tables:
                    list_tables=[val.strip().strip("\"\'") for val in options.tables.split(',')]
                if options.views:
                    list_views=[val.strip().strip("\"\'") for val in options.views.split(',')]
            except:
                print u'请使用英文半角逗号分隔database列表和table列表。'
            else:
                self.cut(filename=filename, ignore_case=options.ignore, list_database=list_database, list_table=list_tables,list_view=list_views)

        else:
            parser.print_help()
    
    
    
    
if __name__=='__main__':
    cut=CutDumpedSql()
    cut.work()

    


