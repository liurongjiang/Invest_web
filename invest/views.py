#coding=utf-8
import re, json, yaml, logging
from invest import invest
from util.sql_tools import *
from flask import request, render_template
from database.my_mysql import MysqlHandler
from flask_login import current_user, login_required
from util.my_time import c_date_time
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
    #通过搜索服务取得数据，不再走mysql
    query_sql, count_sql, resp = query_list(args)
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
    query_sql='SELECT * FROM matrix_invest_project WHERE matrix_id="%s";' % args.get('matrix_id')
    docs = mysql.query(query_sql)
    if not docs:
        query_sql='SELECT * FROM holding_detect_company WHERE matrix_id="%s";' % args.get('matrix_id')
        docs = mysql.query(query_sql)
    return json.dumps( docs )

@invest.route('/team_list', methods=('GET', 'POST'))
def team_list():
    args=request.args
    query_sql='SELECT * FROM matrix_invest_team WHERE matrix_id="%s";' % args.get('matrix_id')
    docs = mysql.query(query_sql)
    return json.dumps( docs )

@invest.route('/event_list', methods=('GET', 'POST'))
def event_list():
    args=request.args
    query_sql='SELECT * FROM matrix_invest_event WHERE matrix_id="%s" ORDER BY finance_date DESC;' % args.get('matrix_id')
    docs = mysql.query(query_sql)
    resp={}
    resp['data']=docs
    resp['recordsTotal']=len(docs)
    resp['recordsLength']=len(docs)
    resp['recordsFiltered']=len(docs)
    return json.dumps( resp )


@invest.route('/log/check_record/<string:record_id>', methods=('GET', 'POST'))
def check_record(record_id):
    '''
        用户行为统计分析。
        存储当前时间、username、project_id
    '''
    insert_sql='INSERT INTO matrix_project_scan (`username`, `project_id`, `scan_date_time`) VALUES ("%s", "%s", "%s")' % (current_user.username, record_id, c_date_time())
    mysql.insert( insert_sql )
    logger.info('{} checked record_id {}'.format(current_user.username, record_id))
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}

@invest.route('/receiptor')
def receipte():
    resp = {'status': 200, 'msg': 'success!!!'}
    try:
        username=request.args.get('username')
        matrix_id=request.args.get('matrix_id')
        update_sql='UPDATE matrix_invest_project SET receiptor="%s", status=2 WHERE matrix_id="%s";' % (username, matrix_id)
        mysql.update(update_sql)
        update_sql='UPDATE holding_detect_company SET receiptor="%s", status=2 WHERE matrix_id="%s";' % (username, matrix_id)
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