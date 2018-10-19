#coding=utf-8
import re, json, yaml, logging
from invest import invest
from util.sql_tools import *
from flask import request, render_template
from database.my_mysql import MysqlHandler
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

@invest.route('/content', methods=('GET', 'POST'))  #指定路由为/，因为run.py中指定了前缀，浏览器访问时，路径为http://IP/asset/
@login_required
def project_content():
    return render_template('invest/content.html',user=current_user)  #返回index.html模板，路径默认在templates下

@invest.route('/invest_json', methods=('GET', 'POST'))
def invest_json():
    args=request.args
    table_name='matrix_invest_project'
    
    #通过搜索服务取得数据，不再走mysql
    query_sql, count_sql, resp = query_list(table_name, args)
    if resp is not None: return json.dumps(resp)

    docs = mysql.query(query_sql)
    count = mysql.query(count_sql)

    resp={}
    resp['data']=docs
    count=count[0]['COUNT(1)'] if count else 0
    resp['recordsTotal']=count
    resp['recordsLength']=count
    resp['recordsFiltered']=count

    return json.dumps(resp)

@invest.route('/project_json', methods=('GET', 'POST'))
def project_json():
    args=request.args
    query_sql='SELECT * FROM matrix_invest_project WHERE %s' % args.get('id')
    docs = mysql.query(query_sql)
    return json.dumps( docs )

@invest.route('/team_json', methods=('GET', 'POST'))
def team_json():
    args=request.args
    query_sql='SELECT * FROM matrix_invest_team WHERE %s' % args.get('id')
    docs = mysql.query(query_sql)
    return json.dumps( docs )

@invest.route('/log/check_record/<int:record_id>', methods=('GET', 'POST'))
def check_record(record_id):
    logger.info('{} checked record_id {}'.format(current_user.username, str(record_id)))
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}

@invest.route('/receiptor')
def receipte():
    resp = {'status': 200, 'msg': 'success!!!'}
    try:
        username=request.args.get('username')
        matrix_id=request.args.get('matrix_id')
        update_sql='UPDATE matrix_invest_project SET receiptor="%s" WHERE matrix_id="%s";' % (username, matrix_id)
        mysql.update(update_sql)
        try:
            insert_sql='INSERT INTO matrix_invest_feedback (`matrix_id`, `user_name`, `feedback_desc`) VALUES ("%s", "%s", "")' % (matrix_id, username)
            mysql.insert(insert_sql)
        except Exception as e:
            print( e )
    except Exception as e:
        resp['status']=0
        resp['statmsgus']= '%s' % e
    return json.dumps(resp)

@invest.route('/feedback', methods=('GET', 'POST'))
def feedback():
    resp = {'status': 200, 'msg': 'success!!!', 'data': {}}
    if request.method == 'GET':
        #query()
        matrix_id=request.args.get('matrix_id')
        query_sql='SELECT feedback_desc FROM matrix_invest_feedback WHERE matrix_id="%s";' % matrix_id.strip()
        result=mysql.query(query_sql)
        resp['data']={'feedback_desc': result[0]['feedback_desc']}
    elif request.method == 'POST':
        #submit
        try:
            matrix_id=request.args.get('matrix_id')
            desc=request.args.get('desc')
            update_sql='UPDATE matrix_invest_feedback SET feedback_desc="%s" WHERE matrix_id="%s";' % (desc, matrix_id)
            mysql.update(update_sql)
        except Exception as e:
            resp['status']=0
            resp['msg']= '%s' % e
    return json.dumps(resp)