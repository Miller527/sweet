#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Miller"
# Date: 2018/12/13

# 负责控制curd的中间件和认证规则
from sanic import Sanic, Blueprint

from curd.control import _AdminConfig
from rbac.views import login, verify_login, logout, test_login, test_verify_login, \
    test_logout, test_ldap_verify_login, ldap_verify_login

from .middleware import login_middle


class RBACConfigObjError(Exception):
    def __init__(self, msg: str):
        self.message = msg

    def __str__(self):
        return f"RBACConfigObjError: '{self.message}' type is Error."


class RBACConfigObjParamError(Exception):
    def __init__(self, msg: str):
        self.message = msg

    def __str__(self):
        return f"RBACConfigObjParamError: param '{self.message}' is Error."


def RbacConfig(curd: _AdminConfig = None, index: bool = False, ldap: bool = False, mode: bool = False):
    """
    配置RBAC注入CURD
    :param curd: 配置对象
    :param index: 是否更改登录
    :param ldap: 是否使用ldap认证
    :param mode: 开发使用
    """
    if not curd:
        raise RBACConfigObjError("CURD")

    if isinstance(curd, Sanic):
        return

    if isinstance(curd, Blueprint):
        return

    if hasattr(curd, "AccessControl"):
        curd.AccessControl = "rbac"
    else:
        raise RBACConfigObjParamError("AccessControl")

    if hasattr(curd, "VerifyLoginFunc"):
        if ldap:
            curd.VerifyLoginFunc = test_ldap_verify_login if mode else ldap_verify_login
        else:
            curd.VerifyLoginFunc = test_verify_login if mode else verify_login
    else:
        raise RBACConfigObjParamError("VerifyLoginFunc")

    if hasattr(curd, "LogoutFunc"):
        curd.LogoutFunc = test_logout if mode else logout
    else:
        raise RBACConfigObjParamError("VerifyLoginFunc")

    if index:
        if hasattr(curd, "LoginFunc"):
            curd.LoginFunc = test_login if mode else login
        else:
            raise RBACConfigObjParamError("LoginFunc")

    curd.add_request_middleware(login_middle)
    curd.add_write("/manager/login", "/favicon.ico", "/manager/verify-login", "/manager/login-slide-code", "/manager/logout")
