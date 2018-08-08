#coding=utf-8
import re, json, yaml
from invest import invest
from util.sql_tools import *
from flask import request, render_template
from database.my_mysql import MysqlHandle

mysql_settings=yaml.load(open('./yamls/mysql.yaml'))
mysql=MysqlHandle(mysql_settings)

@invest.route('/list', methods=('GET', 'POST'))  #指定路由为/，因为run.py中指定了前缀，浏览器访问时，路径为http://IP/asset/
def invest_list():
    print('__name__', __name__)
    return render_template('invest/list.html')  #返回index.html模板，路径默认在templates下

@invest.route('/invest_json', methods=('GET', 'POST'))
def invest_json():
    args=request.args
    table_name='invest_event_info'
    
    query_sql, count_sql = query_list(table_name, args)
    docs = mysql.query(query_sql)
    count = mysql.query(count_sql)

    resp={}
    resp['data']=docs
    count=count[0]['COUNT(1)'] if count else 0
    resp['recordsTotal']=count
    resp['recordsLength']=count
    resp['recordsFiltered']=count

    return json.dumps(resp)

@invest.route('/test', methods=('GET', 'POST'))
def test():
    return '1111'
