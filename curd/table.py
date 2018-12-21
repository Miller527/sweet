#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Miller"
# Date: 2018/12/10

from sanic import Blueprint

class TableConfig(object):
    # 数据库的字段
    field = []
    # 显示的字段
    title = []
    # 扩展的url
    urls = {}
    # 前端表的配置信息
    config = {}

    @staticmethod
    def check_url(url: str):
        while url.startswith("/"):
            url = url[1:]
        while url.endswith("/"):
            url = url[:-1]
        return url

    def extend_url(self, name: str, bp: Blueprint):
        for url, func in self.urls.items():
            bp.add_route(func, f"/{name}/{self.check_url(url)}")


if __name__ == '__main__':
    a = "/bbb///"
    while a.endswith("/"):
        a = a[:-1]
    print(a)
