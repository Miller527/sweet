#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Miller"
# Date: 2018/12/12

import os
import warnings
from .table import TableConfig
from .utils.string import camel_string

_path = os.path.dirname(__file__)


class TableExistedWarning(Warning):
    def __init__(self, msg: str):
        self.message = msg

    def __str__(self):
        return f"TableConfig '{self.message}' already exist."


class ElementExistedWarning(Warning):
    def __init__(self, msg: str):
        self.message = msg

    def __str__(self):
        return f"CustomSet '{self.message}' already exist."


class AccessControlError(Exception):
    def __str__(self):
        return "_AdminConfig AccessControl settings Error."


class TemplateTypeError(Exception):
    def __init__(self, msg: str):
        self.message = msg

    def __str__(self):
        return f"TemplateTypeError: '{self.message}' type is not supported."

class ParamTypeError(Exception):
    def __init__(self, msg: str):
        self.message = msg

    def __str__(self):
        return f"ParamTypeError: '{self.message}' type is not supported."


class BehaviorLogTypeError(Exception):
    def __init__(self, msg: str):
        self.message = msg

    def __str__(self):
        return f"BehaviorLogTypeError: '{self.message}' type is not supported."


class _CustomSet(object):
    def __init__(self):
        self.value = []

    def add(self, *element: str):
        for ele in element:
            if ele in self.value:
                warnings.warn(ElementExistedWarning(ele))
                continue
            self.value.append(ele)

    def delete(self, *element: str):
        for ele in element:
            self.value.remove(ele)

    def __iter__(self):
        for val in self.value:
            yield val

    def is_in(self, element: str) -> bool:
        if element in self.value:
            return True
        return False

    def __str__(self):
        return self.value.__str__()


class _AdminConfig(object):
    def __init__(self):
        self._access_control = "static"
        self._prefix = "manager"
        self._extend = "curd"
        self._bp_name = "curd"
        self._relative = "<name:[A-z]+>"  # 写死
        self._template = "app"
        self._template_path = _CustomSet()
        self._template_path.add(os.path.join(_path, 'template'))
        self._white_urls = _CustomSet()
        self._black_urls = _CustomSet()
        self._login_func = None
        self._logout_func = None
        self._listener = False
        self._db_conn_params = {}
        self._verify_login_func = None
        self._behavior_log_type = "mysql"
        self.Registry = {}
        self._app_middle = {
            "request": _CustomSet(),
            "response": _CustomSet(),
        }

        self.Query = None
        self.BehaviorLog = None
        self. _session_left_salt= "curd"
        self._session_right_salt = "rbac"
        self._session_expire = 600
        # self._buttons = _CustomSet()
        # self._global_middlewares = _CustomSet()
        # self._group_middlewares = _CustomSet()

    @property
    def SessionLeftSalt(self):
        return self._session_left_salt

    @SessionLeftSalt.setter
    def SessionLeftSalt(self, val: str):
        if not isinstance(val, str):
            raise ParamTypeError("SessionLeftSalt")
        self._session_left_salt = val

    @property
    def SessionRightSalt(self):
        return self._session_right_salt

    @SessionRightSalt.setter
    def SessionRightSalt(self, val: str):
        if not isinstance(val, str):
            raise ParamTypeError("SessionRightSalt")
        self._session_expire = val

    @property
    def SessionExpire(self):
        return self._session_expire

    @SessionExpire.setter
    def SessionExpire(self, val: int):
        if not isinstance(val, int):
            raise ParamTypeError("SessionExpire")
        self._session_right_salt = val


    @property
    def request_middleware(self):
        return self._app_middle.get("request").value

    def add_request_middleware(self, *func):
        self._app_middle.get("request").add(*func)

    def delete_request_middleware(self, *func):
        self._app_middle.get("request").delete(*func)

    @property
    def response_middleware(self):
        return self._app_middle.get("response").value

    def add_response_middleware(self, *func):
        self._app_middle.get("response").add(*func)

    def delete_response_middleware(self, *func):
        self._app_middle.get("response").delete(*func)


    @property
    def BehaviorLogType(self):
        return self._behavior_log_type

    @BehaviorLogType.setter
    def BehaviorLogType(self, val: str):
        if val not in ["mysql", "es"]:
            raise BehaviorLogTypeError(val)
        self._behavior_log_type = val
        self._db_conn_params = {}
    @property
    def Listener(self):
        return self._listener

    @Listener.setter
    def Listener(self, val: bool):
        if not isinstance(val, bool):
            raise ParamTypeError("Listener")
        self._listener = val

    @property
    def MySQLDBConnParams(self):
        return self._db_conn_params

    @MySQLDBConnParams.setter
    def MySQLDBConnParams(self, val: dict):
        self._db_conn_params = val

    @property
    def Template(self):
        return self._template

    @Template.setter
    def Template(self, temp: str):
        if temp not in ["jinja2", "app"]:
            raise TemplateTypeError(temp)
        self._template = temp

    @property
    def BPName(self):
        return self._bp_name

    @BPName.setter
    def BPName(self, bp_name: str):
        self._bp_name = bp_name

    @property
    def TemplatePaths(self):
        return self._template_path.value

    def add_template_path(self, *url: str):
        self._template_path.add(*url)

    def delete_template_path(self, url: str):
        self._template_path.delete(url)

    @property
    def LoginFunc(self):
        return self._login_func if self._login_func else None

    @LoginFunc.setter
    def LoginFunc(self, func):
        self._login_func = func

    @property
    def VerifyLoginFunc(self):
        return self._verify_login_func if self._verify_login_func else None

    @VerifyLoginFunc.setter
    def VerifyLoginFunc(self, func):
        self._verify_login_func = func

    @property
    def LogoutFunc(self):
        return self._logout_func if self._logout_func else None

    @LogoutFunc.setter
    def LogoutFunc(self, func):
        self._logout_func = func

    @property
    def AccessControl(self):
        return self._access_control

    @AccessControl.setter
    def AccessControl(self, val: str):
        self._access_control = val

    @property
    def Prefix(self):
        return self._prefix

    @Prefix.setter
    def Prefix(self, val: str):
        self._prefix = val

    @property
    def Extend(self):
        return self._extend

    @Extend.setter
    def Extend(self, val: str):
        self._extend = val

    @property
    def black_urls(self):
        return self._black_urls.value

    def add_black(self, *url: str):
        self._black_urls.add(*url)

    def delete_black(self, *url: str):
        self._black_urls.delete(*url)

    @property
    def white_urls(self):
        return self._white_urls.value

    def add_write(self, *url: str):
        self._white_urls.add(*url)

    def delete_white(self, url: str):
        self._white_urls.delete(url)

    def check_params(self):
        self._check_prefix()
        self._check_extend()
        self._check_access_control()

    # todo 优化处理算法
    def _check_prefix(self):
        if not self._prefix:
            self._prefix = "/"
            return
        if not self._prefix.startswith("/"):
            self._prefix = f"/{self._prefix}"
        if not self._prefix.endswith("/"):
            self._prefix = f"{self._prefix}/"

    # todo 优化处理算法
    def _check_extend(self):
        if not self._extend:
            self._extend = "/"
            return
        while self._extend.startswith("/"):
            self._extend = self._extend[1:]
        if not self._extend.endswith("/"):
            self._extend = f"{self._extend}/"

    def _check_access_control(self):
        if self.AccessControl not in ["rbac", "static"]:
            raise AccessControlError()

    def register(self, desc, conf: TableConfig):
        """
        注册数据表
        :param desc: 表结构
        :param conf: 表配置
        :return:
        """

        if desc not in self.Registry:
            self.Registry[camel_string(desc.__name__)] = {"desc": desc, "conf": conf}
        else:
            warnings.warn(TableExistedWarning(desc))

    def _verify_name(self, desc):
        """校验数据库表明"""
        name = camel_string(desc.__name__)

    def _verify_field(self, desc):
        """校验数据库字段名"""
        name = camel_string(desc.__name__)

    def verify(self, desc):
        self._verify_name(desc)
        self._verify_field(desc)


AdminConfig = _AdminConfig()


def new_admin_config():
    return _AdminConfig()
