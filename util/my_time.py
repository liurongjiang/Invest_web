#coding=utf-8
import time

def c_date():
    return time2date(time.time())

def c_date_time():
    return time2date_time(time.time())

def c_time():
    return time.time()

def date2time(str_date):
    return time.mktime(time.strptime(str_date,'%Y-%m-%d'))

def date_time2time(str_date):
    return time.mktime(time.strptime(str_date,'%Y-%m-%d %H:%M:%S'))

def time2date(number):
    return time.strftime('%Y-%m-%d', time.localtime(number))

def time2date_time(number):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(number))