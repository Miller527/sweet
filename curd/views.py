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
    # todo 填充link数据， 放在这是因为协程不能遍历
    for k, v in AdminConfig.Registry.items():
        link_field_list = v["desc"].link_field()
        if not link_field_list:
            continue
        for key in link_field_list:
            field = v["desc"].get_field(key)
            await field.get_link_data()
    return HtmlResponse(request, "rbac.html", tables=AdminConfig.Registry, sorted_list=AdminConfig.RegistrySorted)


# 添加, /xxx/<name>/add?id=[1,2]&name=[a,b]&age=[15,16]
# 全字段
async def add(request, name):
    """添加, 单条和多条"""
    x = AdminConfig.Registry.get(name)
    if not x:
        return JsonResponse({"status": 403, "msg": "add"})

    field = x["desc"].all_field()
    val = ["'%s'" % request.form.get(k) for k in field]
    sql = f"""
    INSERT INTO {name} ( {",".join(field)} )
                       VALUES
                       ( {",".join(val)} )
    """
    result = await AdminConfig.Query.insert(sql)
    return JsonResponse({"status": 200, "msg": "add", "id": result})


# 查询列表，/xxx/<name>/delete?id=[1,2,3,4]
# return 成功状态
async def delete(request, name):
    """删除, 单条和多条"""
    ids = request.form.getlist("ids")

    sql = f"""
        DELETE FROM {name} WHERE id IN ({",".join(ids)})
    """
    result = await AdminConfig.Query.delete(sql)
    if not result:
        return JsonResponse({"status": 400, "msg": "delete error"})

    return JsonResponse({"status":200, "msg": "delete success"})


# 更新, /xxx/<name>/update?id=[1,2]&name=[a,b]
async def update(request, name):
    return JsonResponse({"msg": "listed"})


# 查询列表，/xxx/<name>/list?page=1
# return 所有行数据, 角色权限过滤
async def listed(request, name):
    if name not in AdminConfig.Registry:
        return JsonResponse({"data": []})
    conf = AdminConfig.Registry[name]["conf"]
    fields = conf.field
    fields_str = ",".join(fields)
    if "updown" in conf.operate:
        fields_str = fields_str + "," + "updown"

    result = await AdminConfig.Query.select(f"select {fields_str} from {name}")

    # from curd.table import TableConfig
    # conf = TableConfig()
    data = []
    for l in result:
        line = []
        l_id = l.get("id")
        if conf.left:
            line.append(f'<input class="checkline" type="checkbox" value="{l_id}">')
        for f in fields:
            line.append(l.get(f))

        if conf.right:
            opt = ""
            for k in conf.operate:
                if k == "updown":
                    status_str = conf.operate_html.get(k, {}).get(str(l.get(k)))
                    opt += status_str.format(id=l_id, name=name)

                else:
                    opt += conf.operate_html.get(k).format(id=l_id, name=name)
            line.append(opt)
        data.append(line)
    return JsonResponse({"data": data})


# 查询一条数据的详情，/xxx/<name>/detail?id=1
# return 详情数据和表结构, json方式
async def detail(request, name, pk):
    return JsonResponse({"msg": "detail"})


async def slide_code(request):
    width = 360
    height = 176
    img = [
        '/static/slide_code/images/ver-0.png',
        '/static/slide_code/images/ver-1.png',
        '/static/slide_code/images/ver-2.png',
        '/static/slide_code/images/ver-3.png',
    ]
    img_src = random.choice(img)

    pl_size = 48
    padding = 20
    _min_x = pl_size + padding
    _max_x = width - padding - pl_size - pl_size // 6
    _min_y = height - padding - pl_size - pl_size // 6
    _max_y = padding
    deviation = 4  # 滑动偏移量

    x = random_num(_min_x, _max_x)
    y = random_num(_min_y, _max_y)
    request["session"]["coords"] = [x - 10 - deviation, x - 10 + deviation]
    request["session"]["coordY"] = y
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
