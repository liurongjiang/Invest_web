#coding=utf-8
from my_time import *
from util.es_search import search_by_elasticsearch
from util.date_regex_handler import investDateHandler

def query_list(table_name, args):
    KEYWORDS = args.get('keyWords') or None

    LENGTH=args.get('length') or 10
    START = args.get('start') or 0
    if KEYWORDS: 
        return None, None, search_by_elasticsearch(KEYWORDS, START, LENGTH)
    INDUSTRY = args.get('industry') or None
    ROUND = args.get('round') or None
    REGION = args.get('region') or None
    SOURCE = args.get('source') or None
    INVESTDATE = args.get('investDate') or None
    LIMIT=' LIMIT %s, %s' % (START, LENGTH)
    order_colum_index=args.get('order[0][column]')
    ORDER_KEY='finance_time'
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
        dateLs=INVESTDATE.split('/')
        startDate=investDateHandler(dateLs[0])
        startDateTime=date2time(startDate)
        WHERES.append('finance_time >= %s' % startDateTime)
        if len(dateLs)==2 and dateLs[1]:
            endDate=investDateHandler(dateLs[1])
            endDateTime=date2time(endDate)
            WHERES.append('finance_time <= %s' % endDateTime)

    if INDUSTRY:
        WHERES.append('industry="%s"' % INDUSTRY)

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
    
    if SOURCE:
        if SOURCE == '工商':
            WHERES.append('source="%s"' % SOURCE)
        else:
            WHERES.append('source !="工商"')

    ''' 
        @该部分调整为通过es搜索
        if KEYWORDS:
            keyInfo = ' (project_name LIKE "%'+ KEYWORDS.strip() + '%" OR company_name like"%'+ KEYWORDS.strip() +'%")'
            WHERES.append(keyInfo)
    '''

    if WHERES:
        WHERE += ' WHERE ' + ' AND '.join(WHERES)
    ORDER_BY=' ORDER BY %s %s' % (ORDER_KEY, ORDER_DIR)

    query_sql='SELECT * ' + FROM + WHERE + ORDER_BY + LIMIT + ';'
    count_sql='SELECT COUNT(1) ' + FROM + WHERE + ';'
    return query_sql, count_sql, None



