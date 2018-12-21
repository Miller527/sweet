#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Miller"
# Date: 2018/12/10
import random

from .handler.responce import html as HtmlResponse, AdminConfig
from sanic.response import json as JsonResponse, redirect as RedirectResponse


async def index(request):
    """curd主页"""
    return HtmlResponse(request, "index.html")


async def login(request):
    """登录"""
    print("AdminConfig.TemplatePaths", AdminConfig.TemplatePaths)

    return HtmlResponse(None, "login.html")


async def logout(request):
    """登出"""

    return RedirectResponse(request.app.url_for(f"{AdminConfig.BPName}.login"))


async def verify_login(request):
    """验证登录"""
    print(request.form.get)
    return JsonResponse({"msg": "verify_login"})


async def table_index(request, name):
    """单表详情"""
    return HtmlResponse(".html")


async def multi_table_index(request):
    """单表详情"""
    print(AdminConfig.Template)
    return HtmlResponse(request, "table.html", tables=AdminConfig.Registry)


# 添加, /xxx/<name>/add?id=[1,2]&name=[a,b]&age=[15,16]
# 全字段
async def add(request, name):
    """添加, 单条和多条"""
    return JsonResponse({"msg": "add"})


# 查询列表，/xxx/<name>/delete?id=[1,2,3,4]
# return 成功状态
async def delete(request, name):
    """删除, 单条和多条"""
    return JsonResponse({"msg": "delete"})


# 更新, /xxx/<name>/update?id=[1,2]&name=[a,b]
async def update(request, name):
    return JsonResponse({"msg": "listed"})


# 查询列表，/xxx/<name>/list?page=1
# return 所有行数据, 角色权限过滤
async def listed(request, name):
    x = await AdminConfig.Query.select("select `id` from role")
    # print(x)
    return JsonResponse({"data": x})


# 查询一条数据的详情，/xxx/<name>/detail?id=1
# return 详情数据和表结构, json方式
async def detail(request, name, pk):
    return JsonResponse({"msg": "detail"})


async def slide_code(request):
    print("zxzxzxzxzxzxzxzx")
    width = 360
    height = 176
    img = [
              '/static/slide_code/images/ver-0.png',
              '/static/slide_code/images/ver-1.png',
              '/static/slide_code/images/ver-2.png',
              '/static/slide_code/images/ver-3.png',
          ]
    img_src = random.choice(img)
    print(img_src)

    pl_size = 48
    padding = 20
    _min_x = pl_size + padding
    _max_x = width - padding - pl_size - pl_size // 6
    _min_y = height - padding - pl_size - pl_size // 6
    _max_y = padding
    deviation = 4 # 滑动偏移量

    x = random_num(_min_x, _max_x)
    y = random_num(_min_y, _max_y)
    request["session"]["coords"] = [x-10-deviation,x-10 +deviation]
    return JsonResponse({"width": width, "height": height,
                         "img_src": img_src, "pl_size": pl_size,
                         "padding": padding, "x": x, "y": y,
                         "deviation": deviation
                         })


def random_num(mi, ma):
    rang = ma - mi
    rand = random.random()
    if round(rand * rang) == 0:
        return mi + 1
    elif round(rand * ma) == ma:
        return ma - 1
    else:
        return mi + round(rand * rang) - 1
