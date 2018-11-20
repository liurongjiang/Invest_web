#coding=utf-8
import re

def investDateHandler(string):
    regx='(?P<year>\d{4})\D?(?P<month>\d*)\D?(?P<day>\d*)'
    result=re.search(regx, string)
    if result is None: return None
    year=result.group('year')
    month=result.group('month')
    day=result.group('day')
    if len(month) < 2:
        if len(month)==0:
            month='01'
        else:
            month = '0' + month
    if len(day) < 2:
        if len(day)==0:
            day='01'
        else:
            day = '0' + day
    return '%s-%s-%s' % (year, month, day)