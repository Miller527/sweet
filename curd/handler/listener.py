#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Miller"
# Date: 2018/12/12
import aiomysql
from aiomysql import DictCursor
from sanic import Sanic

from ..db import MySQLDB
from ..es import ElasticSearchDB
from ..control import AdminConfig


def add_listen(app):
    app.register_listener(before_server_start, "before_server_start")
    return app


async def before_server_start(app: Sanic, loop):
    """
    服务启动前，预处理
    :param app:
    :param loop:
    :return:
    """
    if AdminConfig.Listener:
        pool = await aiomysql.create_pool(loop=loop,maxsize=10, pool_recycle=3, cursorclass=DictCursor, **AdminConfig.MySQLDBConnParams)
        AdminConfig.Query = MySQLDB(pool=pool)
        if AdminConfig.BehaviorLog == "mysql":
            AdminConfig.BehaviorLog = AdminConfig.Query
        else:
            AdminConfig.BehaviorLog = ElasticSearchDB()
