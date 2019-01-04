#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Miller"
# Date: 2018/12/13
import re

from sanic.response import redirect as RedirectResponse, html

from curd.control import AdminConfig


def regex_url(url, regex_list):
    for re_str in regex_list:
        if re.fullmatch(r"%s" % re_str, url):
            return True
    return False


async def login_middle(request):
    if request.path.endswith("/"):
        url_path = request.path[:-1]
    else:
        url_path = request.path
    permission = request["session"].get("permission", {})
    # todo, 打印 session 内容，有访问权限的url
    # print("permission---------------->", permission)
    if url_path not in AdminConfig.white_urls and "static" not in url_path:
        if not permission:
            return RedirectResponse("/manager/login")
        if url_path not in permission.get("static", []) and not regex_url(url_path, permission.get("regex", [])):
            return html("403")
        # print(request["session"].get("miller"))
    else:
        if url_path == "/manager/login" and request["session"].get("menu"):
            return RedirectResponse("/manager/index")
