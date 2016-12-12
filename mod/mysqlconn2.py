import mysql.connector


class MysqlConnection(object):

    def __init__(self, host='', user='', db='', password='',  port=3358, timeout=3):
        self.config = {
            'user': user.strip(),
            'password': password,
            'host': host.strip(),
            'port': int(port),
            'database': db.strip(),
            'raise_on_warnings': True,
        }
        self.conn = None

    def __del__(self):
        try:
            self.cursor.close()
            self.conn.ping(False)
            self.conn.close()
        except Exception, e:
            pass

    def connect(self):
        if self.conn is None:
            self.conn = mysql.connector.connect(**self.config)
            self.cursor = self.conn.cursor(dictionary=True)

    def execute(self, sql, args=None):
        self.connect()
        self.cursor.execute(sql, args)
        ret = self.cursor.fetchall()
        self.conn.commit()
        return ret

    def executemany(self, sql, args):
        self.connect()
        self.cursor.executemany(sql, args)
        self.conn.commit()
        return 0

    def query(self, sql, args=None):
        return self.execute(sql, args)
