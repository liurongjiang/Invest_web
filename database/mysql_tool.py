#coding=utf-8
from . import pymysql_pool

class MysqlHandler():
    
    def __init__(self):
        pymysql_pool.logger.setLevel('DEBUG')
        config={'host':'192.168.1.180', 
                'user':'rongjiang', 
                'password':'password4321', 
                'database':'integrated'}
        self.pool = pymysql_pool.ConnectionPool(size=20, name='pool', **config)

    def query(self, query_sql):
        results=[]
        conn=self.pool.get_connection()
        print('__query_sql: ', query_sql)

        try:
            with conn as cursor:
                cursor.execute(query_sql)
                description = cursor.description
                if description:
                    keys=[]
                    for tup in description:
                        keys.append(tup[0])
                    fetch = cursor.fetchall()
                    for res_tup in fetch:
                        dic={}
                        for index in range(0, len(res_tup)):
                            dic[keys[index]]=res_tup[index]
                    results.append(dic)
                else:
                    print( '__err: description is: ', description )
        except Exception as e:
            print( e )
        finally:
            self.pool.put_connection(conn)
            print( len( results ) )
            return results

    def update(self, update_sql):
        print('___update_insert_sql: ', update_sql)
        conn=self.pool.get_connection()
        try:
            with conn as cursor:
                cursor.execute(update_sql)
                conn.commit()
        except Exception as e:
            print( e )
        finally:
            self.pool.put_connection(conn)
        
    def insert(self, inset_sql):
        self.update(inset_sql)

if __name__=='__main__':
    mysql=MysqlHandler()
    res = mysql.query('SELECT * FROM invest_event_info limit 0, 1')
    print( res )