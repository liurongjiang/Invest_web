#coding=utf-8
import time

def c_date():
    return time2date(time.time())

def c_time():
    return time.time()

def date2time(str_date):
    return time.mktime(time.strptime(str_date,'%Y-%m-%d %H:%M:%S'))

def time2date(number):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(number))