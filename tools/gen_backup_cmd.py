# coding:utf8
import time
import re
import os
import sys
import json
DICT_TABLE = {}
import logging


def mylogger(file=None, level='debug'):
    u'''
    modified on 2013.1.11
    this function return a logging.RootLogger object,
    which uses function error(str) or exception(e)
    for recording your log in file
    '''
    import logging
    if file is None:
        return logging
    LEVELS = {'debug': logging.DEBUG, 'info': logging.INFO,
              'warning': logging.WARNING, 'error': logging.ERROR, 'critical': logging.CRITICAL}
    logger = logging.getLogger()
    formatter = logging.Formatter(
        '%(asctime)s %(threadName)s %(funcName)s line:%(lineno) -8s%(levelname)-8s %(message)s ', ' %Y-%m-%d %H:%M:%S')
    try:
        file_handler = logging.FileHandler(file)
    except Exception, e:
        print 'log failed'
        return None
    else:
        file_handler.setFormatter(formatter)
        stream_handler = logging.StreamHandler(sys.stderr)
        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)
        logger.setLevel(LEVELS.get(level))
    logger.removeHandler(stream_handler)  # debug(indicate to eclipse)
    return logger

log = mylogger(os.path.realpath(__file__) + '.log', level='debug')


def get_tables(CURRENT_DB, FILE_SQL):
    f = open(FILE_SQL)
    lines = f.readlines()
    # lines = [
    #     "UPDATE settlement SET status = 5,yn = 0 WHERE settlement_no IN (54077,77573,82246,104664,273899,302604,279175);",
    #     "DELETE FROM settlement_history WHERE settlement_no IN (54077,77573,82246,104664);"
    # ]
    for line in lines:
        if line.strip():
            s = re.search('^\s*update\s+(?P<tname>\w+)\s+set\s+.*(?P<where>\s+WHERE\s+.+)\s*(limit.*)*;*', line.strip(), re.I) \
                or \
                re.search(
                '^\s*delete\s+from\s+(?P<tname>\w+)(?P<where>\s+WHERE\s+.+)\s*(limit.*)*;*', line.strip(), re.I)
            table = s.group('tname')
            where = s.group('where').replace(' WHERE ', '')

            if not DICT_TABLE.has_key(table.strip()):
                DICT_TABLE[table.strip()] = {
                    'where': [where and where.rstrip(';') or ''], 'origin': line}
            else:
                DICT_TABLE[table.strip()]['where'] .append(where and where.rstrip(
                    ';') or '')
                DICT_TABLE[table.strip()]['origin'] = line


def gen_backup_mysqldump_cmd(CURRENT_DB, FILE_SQL):

    for t in DICT_TABLE.keys():
        where = DICT_TABLE[t]['where']
        origin = DICT_TABLE[t]['origin']
        sql1 = '/export/servers/mysql/bin/mysqldump -u root -p --single-transaction --master-data=2 %s %s -w %s >/export/data/mysql/dumps/%s.%s_%s.sql' % (
            CURRENT_DB.strip(), t, json.dumps(' and '.join(where) or '1=1'), CURRENT_DB.strip(), t, time.strftime('%Y%m%d%M%S', time.localtime()))
        print '###############################################'
        print sql1

        log.debug('origin:' + origin)
        log.debug('gen sql:' + sql1)


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option(
        "-B", action='store', type='string', dest="database", default=None, help=u'操作的数据库名称')
    parser.add_option(
        "-f", action='store', type='string', dest="filename", default=None, help=u'SQL脚本文件')
    parser.description = u'''example: python %s -B database_name -f sql_script_file''' % __file__
    (options, args) = parser.parse_args()
    if not options.database or not options.filename:
        parser.print_help()
    else:
        CURRENT_DB = options.database
        FILE_SQL = options.filename
        get_tables(CURRENT_DB, FILE_SQL)
        gen_backup_mysqldump_cmd(CURRENT_DB, FILE_SQL)

