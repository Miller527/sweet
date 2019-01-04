#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Miller"
# Date: 2018/12/12

from sanic import response

from jinja2 import Environment, select_autoescape, FileSystemLoader,Markup

from ..control import AdminConfig

if AdminConfig.Template == "app":
    # todo 走静态模版, 需要自己优化
    def html(request, tpl, **kwargs):
        return response.html(tpl)

else:
    _env = Environment(
        loader=FileSystemLoader(AdminConfig.TemplatePaths),
        autoescape=select_autoescape(['html', 'xml', 'tpl'])
    )

    def html(request, tpl, **kwargs):
        if request:
            kwargs["left_menu"] = request["session"].get("menu")
            kwargs["username"] = request["session"]["account_name"]
        temp = _env.get_template(tpl)
        return response.html(temp.render(kwargs))


