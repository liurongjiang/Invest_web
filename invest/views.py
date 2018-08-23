#coding=utf-8
import re, json, yaml, logging
from invest import invest
from util.sql_tools import *
from flask import request, render_template
from database.mysql_tool import MysqlHandler
#from database.my_mysql import MysqlHandle
#mysql_settings=yaml.load(open('./yamls/mysql.yaml'))
#mysql=MysqlHandle(mysql_settings)
from flask_login import current_user, login_required

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)s:%(levelname)s:%(asctime)s:%(message)s')
file_handler = logging.FileHandler('logs/invest.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

mysql=MysqlHandler()

@invest.route('/list', methods=('GET', 'POST'))  #指定路由为/，因为run.py中指定了前缀，浏览器访问时，路径为http://IP/asset/
@login_required
def invest_list():
    print('__name__', __name__)
    return render_template('invest/list.html',user=current_user)  #返回index.html模板，路径默认在templates下

@invest.route('/invest_json', methods=('GET', 'POST'))
def invest_json():
    args=request.args
    table_name='integrated_company'
    
    #通过搜索服务取得数据，不再走mysql
    query_sql, count_sql, resp = query_list(table_name, args)
    if resp: return json.dumps(resp)

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


@invest.route('/log/check_record/<int:record_id>', methods=('GET', 'POST'))
def check_record(record_id):
    logger.info('{} checked record_id {}'.format(current_user.username, str(record_id)))
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}

