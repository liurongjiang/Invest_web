#coding=utf-8
from flask import request, render_template
from database.my_mysql import MysqlHandle
from my_time import *
from util.date_regex_handler import investDateHandler
from invest import invest
import re, json, yaml

mysql_settings=yaml.load(open('./yamls/mysql.yaml'))
mysql=MysqlHandle(mysql_settings)

country_map={
    'gn': 0,
    'gw': 1
}

industry_map={
    'other': u'其它',
    'xfsj': u'消费升级',
    'xjs': u'新技术',
    'qyfw': u'企业服务',
    'whyl': u'文娱+移动2C',
    'jr': u'互联网金融',
    'yl': u'医疗',
    'jy': u'教育',
    'dcx': u'大出行'
}
round_map={
    'zhongzi': u'种子轮',
    'tianshi': u'天使轮',
    'pre_a': u'Pre-A轮',
    'a': u'A轮',
    'a_add': u'A+轮',
    'pre_b': u'Pre-B轮',
    'b': u'B轮',
    'b_add': u'B+轮',
    'c': u'C轮',
    'd': u'D轮',
    'e': u'E轮',
    'f': u'F轮',
    'other': u'其它'
}

@invest.route('/list', methods=('GET', 'POST'))              #指定路由为/，因为run.py中指定了前缀，浏览器访问时，路径为http://IP/asset/
def invest_list():
    print('__name__', __name__)
    return render_template('invest/list.html')  #返回index.html模板，路径默认在templates下

@invest.route('/invest_json', methods=('GET', 'POST'))
def invest_json():
    tableName='invest_event_info'
    #orderBy =
    length=request.args.get('length') or 10
    start = request.args.get('start') or 0
    industry = request.args.get('industry') or None
    _round = request.args.get('round') or None
    country = request.args.get('country') or None
    keyWords = request.args.get('keyWords') or None
    investDate = request.args.get('investDate') or None

    querySql='SELECT * FROM ' + tableName
    countSql='SELECT COUNT(1) FROM ' + tableName

    WHERE = ''
    if industry and industry in industry_map:
        WHERE += ' industry_tags="%s"' % industry_map[industry]
    if _round and _round in round_map:
        if _round=='other':
            roundInfo = 'turn_level >= 16'
        else:
            roundInfo = ' finance_turn="%s"' % round_map[_round]
        if WHERE: WHERE += ' AND' + roundInfo
        else: WHERE += roundInfo

    if country and country in "gn|gw":
        if country=='gn':
            countryInfo=u' country="中国"'
        elif country=='gw':
            countryInfo=u' country!="中国"'

        if WHERE: WHERE += ' AND' + countryInfo
        else: WHERE += countryInfo

    if keyWords:
        keyInfo = ' (project_name LIKE "%'+ keyWords.strip() + '%" OR company_name like"%'+ keyWords.strip() +'%")'
        if WHERE: WHERE += ' AND' + keyInfo
        else: WHERE += keyInfo

    if investDate:
        dateLs=investDate.split('/')
        startDate=investDateHandler(dateLs[0])
        startTime=date2time(startDate)
        investInfo = ' finance_time >= %s' % startTime
        if len(dateLs)==2 and dateLs[1]:
            endDate=investDateHandler(dateLs[1])
            endTime=date2time(endDate)
            investInfo += ' AND finance_time <= %s' % endTime
        if WHERE: WHERE += ' AND' + investInfo
        else: WHERE += investInfo

    if WHERE:
        querySql += ' WHERE' + WHERE
        countSql += ' WHERE' + WHERE

    querySql += ' ORDER BY finance_time DESC LIMIT %s, %s' % (start, length)

    docs = mysql.query(querySql)
    count = mysql.query(countSql)

    print('__querySql: ', querySql)
    resp={}
    resp['data']=docs
    resp['recordsTotal']=count[0]['COUNT(1)'] if count else 0
    resp['recordsLength']=count[0]['COUNT(1)'] if count else 0
    resp['recordsFiltered']=count[0]['COUNT(1)'] if count else 0
    return json.dumps(resp)

@invest.route('/test', methods=('GET', 'POST'))
def test():
    return '1111'