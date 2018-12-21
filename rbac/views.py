#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Miller"
# Date: 2018/12/13
import operator

from curd.control import AdminConfig
from handler.listen_handler import session

from rbac.utils import md5_check

try:
    from curd.handler.responce import html as HtmlResponse
except ImportError:
    from sanic.response import html as HtmlResponse

from sanic.response import redirect as RedirectResponse
from sanic.response import json as JsonResponse


async def login(request):
    """登录页面"""
    print("login page rbac")
    return HtmlResponse(None, "login.html")


async def test_login(request):
    """测试登录页面"""
    print("login rbac")


async def get_menu_permission(menu):
    menu_dict = {}
    static_permission = []
    regex_permission = []
    for line in menu:
        url = line.get("url")
        per_type = line.get("type")
        if per_type is None:
            continue
        if url.endswith("/"):
            static_permission.append(url[:-1]) if per_type == 0 else regex_permission.append(url[:-1])
        else:
            static_permission.append(url) if per_type == 0 else regex_permission.append(url)
        if line.get("is_menu") == 0:
            continue

        if line.get("p_id") == 0:
            menu_id = line.get("id")
            if menu_id not in menu_dict:
                menu_dict[menu_id] = {}
            line.update({"children": []})
            menu_dict[menu_id].update(line)
        else:
            menu_pid = line.get("p_id")
            if menu_pid not in menu_dict:
                menu_dict[menu_pid] = {}
            menu_dict[line.get("p_id")]["children"].append(line)

    menu_list = []
    for _, v in menu_dict.items():
        v["children"] = sorted(v["children"], key=operator.itemgetter('sort'))
        menu_list.append(v)

    return sorted(menu_list, key=operator.itemgetter('sort')), {"static": static_permission, "regex": regex_permission}


async def verify_login(request):
    """基于RBAC内置验证登录"""
    # 写session, 菜单列表写入session
    username = request.form.get("username", "")
    password = request.form.get("password", "")
    coord = int(request.form.get("coord", 0))
    deviation = request["session"].get("coords",[])
    print(coord, deviation)
    print(md5_check("password1",leftsalt="curd",rightsalt="rbac"))
    print(password)
    if not username or not password:
        return JsonResponse({"status": 403, "msg": "请输入正确的用户和密码."})
    if not coord or len(deviation) != 2 or not (deviation[0] < coord < deviation[1]):
        return JsonResponse({"status": 403, "msg": "验证码错误"})

    sql = f'SELECT id,user_name FROM account WHERE user_name="{username}" and passwd="{password}"'
    user_result = await AdminConfig.Query.select(sql, fetchone=True)
    if not user_result or not isinstance(user_result, dict):
        return JsonResponse({"status": 403, "msg": "用户名或密码错误, 请重新输入."})
    user_id = user_result.get("id")
    user_name = user_result.get("user_name")
    if not user_id:
        return JsonResponse({"status": 403, "msg": "用户查询失败."})
    sql = f'SELECT * FROM menu WHERE id in (SELECT menu_id FROM role_menu WHERE role_id' \
        f' in (SELECT role_id FROM role_account WHERE aid="{user_id}")) and status=1'
    result = await AdminConfig.Query.select(sql)
    menu_list, permission = await get_menu_permission(result)
    # sessionid = md5_check(username, leftsalt=AdminConfig.SessionLeftSalt, rightsalt=AdminConfig.SessionRightSalt)
    request["session"]["permission"] = permission
    request["session"]["menu"] = menu_list
    request["session"]["account_id"] = user_id
    request["session"]["account_name"] = user_name
    resp = JsonResponse({"status": 200, "msg": "SUCCESS"})
    # resp.cookies["sessionid"] = sessionid
    return resp


async def test_verify_login(request):
    """验证登录"""
    # 写session, 菜单列表写入session
    print("verify login rbac")


async def ldap_verify_login(request):
    """基于ldap的集中登录认证"""
    print("verify login  rbac ldap")


async def test_ldap_verify_login(request):
    """测试基于ldap的集中登录认证"""
    print("test verify login  rbac ldap")


async def logout(request):
    """退出登录"""
    request["session"].clear()
    return RedirectResponse("login")


async def test_logout(request):
    """验证登录"""
    # 删除session
    print("verify logout rbac")
