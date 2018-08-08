#coding=utf-8
from my_time import *
from util.date_regex_handler import investDateHandler

def query_list(table_name, args):
    LENGTH=args.get('length') or 10
    START = args.get('start') or 0
    INDUSTRY = args.get('industry') or None
    ROUND = args.get('round') or None
    REGION = args.get('region') or None
    KEYWORDS = args.get('keyWords') or None
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
        if REGION != '国外':
            WHERES.append('country="国外"')
        elif REGION=='其它':
            WHERES.append('city_level>10')
        else:
            WHERES.append('city="%s"') % REGION

    if KEYWORDS:
        keyInfo = ' (project_name LIKE "%'+ KEYWORDS.strip() + '%" OR company_name like"%'+ KEYWORDS.strip() +'%")'
        WHERES.append(keyInfo)

    if WHERES:
        WHERE += ' WHERE ' + ' AND '.join(WHERES)
    ORDER_BY=' ORDER BY %s %s' % (ORDER_KEY, ORDER_DIR)

    query_sql='SELECT * ' + FROM + WHERE + ORDER_BY + LIMIT
    count_sql='SELECT COUNT(1) ' + FROM + WHERE
    print('__sql: ', query_sql)
    return query_sql, count_sql