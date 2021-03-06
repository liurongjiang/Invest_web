#coding=utf-8
import re
from my_time import *
from util.es_search import search_by_elasticsearch
from util.date_regex_handler import investDateHandler

industy_map={
    'B2B交易平台': 'B2B交易平台',
    '消费升级/零售': '消费',
    '新技术/智能': '新技术(智能)',
    '文娱/移动2C': '文娱+移动2C',
    '互联网金融/区块链': '互联网金融',
    '企业服务': '企业服务',
    '成长项目': '成长',
    '大出行': '大出行',
    '医疗': '医疗',
    '教育': '教育',
    '区块链': '区块链',
    '其他': '其他'
}

def query_list(args):
    """

    """
    KEYWORDS = args.get('keyWords') or None
    LENGTH=args.get('length') or 10
    START = args.get('start') or 0
    #default__________________________
    SOURCE = args.get('source') or '消息源'
    if SOURCE=='消息源':
        ORDER_KEY='finance_date'
        table_name='matrix_invest_project'
        default_where = ' WHERE finance_turn != "" '
        DOC_TYPE='event'
    elif SOURCE=='工商':
        table_name='holding_detect_company'
        ORDER_KEY='detect_date'
        default_where = ''
        DOC_TYPE='gongshang'
    if KEYWORDS: 
        return None, None, search_by_elasticsearch(KEYWORDS, START, LENGTH, DOC_TYPE)

    INDUSTRY = args.get('industry') or None
    ROUND = args.get('round') or None
    REGION = args.get('region') or None
    INVESTDATE = args.get('investDate') or None
    LIMIT=' LIMIT %s, %s' % (START, LENGTH)
    order_colum_index=args.get('order[0][column]')
    ORDER_DIR='DESC'
    if int(order_colum_index):
        ORDER_KEY=args.get('columns[%s][data]' % order_colum_index)
        ORDER_DIR=args.get('order[0][dir]')

    #1 FROM 
    FROM = ' FROM %s' % table_name

    #2 WHERE
    WHERE=''
    WHERES = []

    if INVESTDATE:
        INVESTDATE=re.sub('00:00:00', '', INVESTDATE)
        dateLs=INVESTDATE.split('/')
        if SOURCE=='工商':
            WHERES.append('detect_date >= "%s"' % dateLs[0].strip())
            if len(dateLs)==2 and dateLs[1]:
                WHERES.append('detect_date <= "%s"' % dateLs[1].strip())
        else:
            startDate=investDateHandler(dateLs[0])
            #startDateTime=date2time(startDate)
            WHERES.append('finance_date >= "%s"' % startDate)
            if len(dateLs)==2 and dateLs[1]:
                endDate=investDateHandler(dateLs[1])
                #endDateTime=date2time(endDate)
                WHERES.append('finance_date <= "%s"' % endDate)

    if INDUSTRY:
        WHERES.append('industry like "%'+ industy_map[INDUSTRY] +'%"')

    if ROUND:
        roundInfo = 'turn_level >= 16' if ROUND=='其它' else ' finance_turn="%s"' % ROUND
        WHERES.append(roundInfo)

    if REGION:
        if REGION == '国外':
            WHERES.append('country="国外"')
        elif REGION=='其它':
            WHERES.append('country="中国" AND city NOT IN ("北京", "上海", "深圳", "杭州", "广州", "成都", "苏州", "南京", "武汉")')
        elif REGION=='国内':
            WHERES.append('country="中国"')
        else:
            WHERES.append('city="%s"' % REGION)

    if WHERES:
        WHERE += ' WHERE ' + ' AND '.join(WHERES)
        if SOURCE=='消息源':
            WHERE += ' AND finance_turn != ""'
    else:
        WHERE=default_where

    ORDER_BY=' ORDER BY %s %s' % (ORDER_KEY, ORDER_DIR)
    query_sql='SELECT *' + FROM + WHERE + ORDER_BY + LIMIT + ';'
    count_sql='SELECT COUNT(1) ' + FROM + WHERE + ';'
    print( query_sql )
    return query_sql, count_sql, None



