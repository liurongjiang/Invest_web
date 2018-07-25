# -*- coding: utf-8 -*-
import sys, yaml, pymysql, pymysql.cursors

class Singleton(object):
    def __new__(cls, *args, **kw):
        if not hasattr(cls, '_instance'):
            orig = super(Singleton, cls)
            cls._instance = orig.__new__(cls, *args, **kw)
        return cls._instance

class MysqlHandle(Singleton):
    '''@ 此处采用单列模式，
       @ 避免过多的实例化。
        '''

    def __init__(self, settings_path="/Users/liurongjiang/Desktop/Invest_web/yamls/default_mysql_conf.yaml"):
        self.settings = yaml.load(open(settings_path))
        self.config = {
            'host':         self.settings['HOST'],
            'port':         self.settings['PORT'],
            'user':         self.settings['USER'],
            'password':     self.settings['PASSWORD'],
            'db':           self.settings['DB'],
            'charset':      self.settings['CHARSET'],
            'cursorclass': pymysql.cursors.DictCursor
        }
        self.conn = self._conn()

    def _conn(self):
        connection = pymysql.connect(**self.config)
        return connection

    def query(self, sql):
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(sql)
                results = cursor.fetchall()
                return results
        except Exception as e:
            print(e)
            return []

    def insert(self, sql):
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(sql)
                self.conn.commit()
        except Exception as e:
            print(e)
            

    def update(self, update_sql):
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(update_sql)
                self.conn.commit()
        except Exception as e:
            print(e)

    def close(self):
        self.conn.close()

if __name__ == '__main__':
    pass