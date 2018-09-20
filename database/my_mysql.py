# -*- coding: utf-8 -*-
from database.pymysqlpool import ConnectionPool

class Singleton(object):
    def __new__(cls, *args, **kw):
        if not hasattr(cls, '_instance'):
            orig = super(Singleton, cls)
            cls._instance = orig.__new__(cls, *args, **kw)
        return cls._instance

class MysqlHandler():
    '''@ 此处采用单列模式，
       @ 避免过多的实例化。
        '''

    def __init__(self, settings=None):
        self.config = {
            'pool_name': 'test',
            'host': '192.168.1.180',
            'port': 3306,
            'user': 'rongjiang',
            'password': 'password4321',
            'database': 'integrated',
            'max_pool_size': 20
        } if settings is None else settings
        
        self.pool = self.connection_pool()

    def connection_pool(self):
        pool = ConnectionPool(**self.config)
        return pool

    def query(self, sql):
        try:
            with self.pool.cursor() as cursor:
                cursor.execute(sql)
                results = cursor.fetchall()
                return results
        except Exception as e:
            print(e)
            return []

    def insert(self, sql):
        try:
            with self.pool.cursor() as cursor:
                cursor.execute(sql)
                self.pool.commit()
        except Exception as e:
            print(e)
            

    def update(self, update_sql):
        try:
            with self.pool.cursor() as cursor:
                cursor.execute(update_sql)
                self.pool.commit()
        except Exception as e:
            print(e)

if __name__ == '__main__':
    pass
