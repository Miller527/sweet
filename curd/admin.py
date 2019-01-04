#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Miller"
# Date: 2018/12/10
import os
import warnings

from sanic import Sanic, Blueprint

from curd.db import MySQLDB
from curd.handler.listener import add_listen
from curd.table import TableConfig
from curd.utils.string import camel_string
from .es import es
from .control import AdminConfig, _AdminConfig,  new_db
from .views import login, index, logout, verify_login, delete, update, listed, add, detail, table_index, \
    multi_table_index, slide_code

lp, mysql = new_db()

class TableExistedWarning(Warning):
    def __init__(self, msg: str):
        self.message = msg

    def __str__(self):
        return f"TableConfig '{self.message}' already exist."

class TableNotFoundError(Exception):
    def __init__(self, msg: str):
        self.message = msg

    def __str__(self):
        return f"TableNotFoundError: table '{self.message}' not found."



class SanicAppError(Warning):
    def __str__(self):
        return f"SanicAppError: App is None or error."


class _AppAdmin(object):

    def __init__(self, ac: _AdminConfig):
        self.Config = ac
        self.Config.check_params()
        self._init_static_url()

    def get_tables(self):
        res = lp.run_until_complete(mysql.select("show tables"))
        for line in res:
            self.Config.add_table(line["Tables_in_eams"])

        print(self.Config.tables)
    # def _init_behavior_log(self):
    #     self.behavior_log = mysql if self.Config.BehaviorLog == "mysql" else es

    def register(self, desc, conf: TableConfig):
        """
        注册数据表
        :param desc: 表结构
        :param conf: 表配置
        :return:
        """
        tb_name = camel_string(desc.__name__)
        if tb_name not in self.Config.tables:
            raise TableNotFoundError(tb_name)
        if tb_name not in self.Config.Registry:
            conf.check()
            conf.length = len(conf.field)

            self.Config.Registry[tb_name] = {"desc": desc, "conf": conf}
        else:
            warnings.warn(TableExistedWarning(desc))

    def _init_static_url(self):
        self._static_url = {
            "verify-login": {
                "handler": self.Config.VerifyLoginFunc if self.Config.VerifyLoginFunc else verify_login,
                "methods": ["POST"],
                "name": "verify-login"
            },
            "index": {
                "handler": index,
                "methods": ["GET"],
                "name": "index"
            },
            "multi_table_index": {
                "handler": multi_table_index,
                "methods": ["GET"],
                "name": "multi_table_index"
            },
            "login-slide-code": {
                "handler": slide_code,
                "methods": ["GET"],
                "name": "login-slide-code"
            },
            "logout": {
                "handler": self.Config.LogoutFunc if self.Config.LogoutFunc else logout,
                "methods": ["GET"],
                "name": "logout"
            },
            "login": {
                "handler": self.Config.LoginFunc if self.Config.LoginFunc else login,
                "methods": ["GET"],
                "name": "login"
            },
        }

    def set_router(self, url: str, func):
        pass

    def middles(self, app: Sanic):
        for v in self.Config.request_middleware:
            app.register_middleware(v, "request")
        for v in self.Config.response_middleware:
            app.register_middleware(v, "response")

    def urls(self, bp: Blueprint):
        """
        初始化蓝图的url
        :param bp:
        :return:
        """

        extend = self.Config.Extend
        if self.Config.AccessControl == "rbac":
            bp.add_route(delete, extend + '<name:string>/delete', methods=['DELETE'])
            bp.add_route(update, extend + '<name:string>/update', methods=['PUT'])
            bp.add_route(listed, extend + '<name:string>/list', methods=['GET'])
            bp.add_route(add, extend + '<name:string>/add', methods=['POST'])
            bp.add_route(detail, extend + '<name:string>/detail/<pk:int>', methods=['GET'])
            bp.add_route(table_index, extend + '<name:string>/index', methods=['GET'])

        else:
            # 遍历注册表
            pass

        for url, info in self._static_url.items():
            print(info.get("handler"), url,
                  info.get("methods"),
                  info.get("name"), id(info.get("handler")))
            bp.add_route(info.get("handler"), url,
                         methods=info.get("methods"),
                         name=info.get("name"))


AppAdmin = _AppAdmin(AdminConfig)
AppAdmin.get_tables()

def new_app_admin(admin_config: _AdminConfig):
    """返回一个新的admin对象, 可用于构建其他蓝图"""
    return _AppAdmin(admin_config)


def init(app: Sanic, app_admin: _AppAdmin = None):
    if not isinstance(app, Sanic):
        raise SanicAppError()
    app_admin = AppAdmin if not app_admin else app_admin
    _bp = Blueprint(app_admin.Config.BPName, url_prefix=app_admin.Config.Prefix)
    # _bp.static('static', os.path.join(_path, 'static'))
    add_listen(app)
    app_admin.urls(bp=_bp)
    app_admin.middles(app=app)
    app.blueprint(_bp)

    app_admin.Config.registry_sorted()
    MySQLDB.clear()

    # app.static('/curd_static', 'curd/static', )
    # if app_admin.Config.BehaviorLog =="mysql":
    #     app_admin.Config.Query = mysql
