#!/usr/bin/env python
# -*- coding: utf-8 -*-
# coding=utf-8
"""
can more db ,more pool
"""
config = {
    'local': {
        'host': "127.0.0.1", 'port': 3306,
        'user': "rongjiang", 'passwd': "password4321",
        'db': "integrated", 'charset': "utf8",
        'pool': {
            # use = 0 no pool else use pool
            "use": 1,
            # size is >=0,  0 is dynamic pool
            "size": 20,
            # pool name
            "name": "local",
        }
    },
    'poi': {
        'host': "192.168.1.180", 'port': 3306,
        'user': "rongjiang", 'passwd': "password4321",
        'db': "integrated", 'charset': "utf8",
        'pool': {
            # use = 0 no pool else use pool
            "use": 1,
            # size is >=0,  0 is dynamic pool
            "size": 20,
            # pool name
            "name": "local",
        }
    },
}