#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Miller"
# Date: 2018/12/10
from enum import Enum

from sanic import Blueprint

from curd.control import new_db, AdminConfig
from curd.utils.string import camel_string

class Field(Enum):
    bool = "bool"
    int = int
    str = str
    float = float
    tuple = tuple
    list = list
    set = set
    dict = dict


class Checker(object):
    # 根据类型字段的输入校验器
    pass


lp, mysql = new_db()


class FieldParams(object):
    # text字符串
    # select, select_data(显示数据，)
    # date时间
    # link关联、link_field(数据字段）、link_table(关联表)
    def __init__(self, name: str, tp, length: int, regex=None, **kwargs):
        self.name = name
        self.type = tp
        self.length = length
        self.regex = regex
        self.kwargs = kwargs
        self._link_data = []

    def select(self):
        data = self.kwargs.get("select_data")
        if data:
            return data
        return [[0, "删除数据"], [1, "正常数据"]]

    async def get_link_data(self):
        link_field = self.kwargs.get("link_field")
        link_table = self.kwargs.get("link_table")
        res = await AdminConfig.Query.select(f'select {",".join(link_field)} from {link_table}')
        self._link_data.append(["0", "无"])
        for line in res:
            li = []
            for field in link_field:
                li.append(line[field])
            self._link_data.append(li)
        print(self._link_data)

    def link(self):
        return self._link_data


class BaseModel(object):

    @classmethod
    def all_field(cls):
        res = []
        for k, v in vars(cls).items():
            if isinstance(v, FieldParams) and "__" not in k:
                res.append(k)

        return res

    @classmethod
    def get_field(cls, key: str):
        if hasattr(cls, key):
            return getattr(cls, key)

    @classmethod
    def link_field(cls):
        res = []
        for k, v in vars(cls).items():
            if isinstance(v, FieldParams) and v.type == "link" and "__" not in k:
                res.append(k)
        return res

    @classmethod
    def string(cls):
        pass

    @classmethod
    def get_name(cls):
        name = cls.string()
        if name:
            return name + "(" + camel_string(cls.__name__) + ")"
        return camel_string(cls.__name__)
class TableConfig(object):
    # 数据库的字段
    field = []
    # 显示的字段, 可以使用表结构上的字段名字
    title = []
    # 扩展的url
    urls = {}
    # # 前端表的配置信息
    # config = {}
    left = None
    right = None

    left_title = ""
    right_title = ""
    #
    length = 0

    operate_html = {
        "updown": {
            "0": '<button class="line_updown"  value="{id}" tbname="{name}" style="color: #FF3030;"><i class="glyphicon glyphicon-ban-circle icon-white"></i></button>',
            "1": '<button class="line_updown"  value="{id}" tbname="{name}" style="color: #66CD00;"><i class="glyphicon glyphicon glyphicon-ok-circle icon-white"></i></button>'
        },
        "detail": '<button class="line_detail"  value="{id}" tbname="{name}"><i class="glyphicon glyphicon-zoom-in icon-white"></i></button>',
        "delete": '<button  class="line_delete" value="{id}" tbname="{name}"><i class="glyphicon glyphicon-trash icon-white"></i></button>',
        "edit": '<button class="line_edit"  value="{id}" tbname="{name}"><i class="glyphicon glyphicon-edit icon-white"></i></button>',

    }
    # （启用、禁用）、（修改、详细）、删除

    operate = ["delete"]

    @classmethod
    def check(cls):
        cls.check_config()

    @classmethod
    def check_config(cls):

        left = """
            <label>
                <input class="checkall" type="checkbox" value="all">
                选择
            </label>
        """

        cls.left_title = left if cls.left and not cls.left_title else ""
        cls.right_title = "操作" if cls.left and not cls.right_title else ""

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

    def check_regex(self):
        """处理字段认证regex"""
        pass

    def check_field(self):
        """判断字段的配置信息"""
        if len(self.field) != len(self.title):
            raise TableConfigError(f"{self.__class__.__name__} field and title inconsistency of length.")

        if len(self.field) == len(self.title) == 0:
            # todo 填充所有字段
            pass


class TableConfigError(Exception):
    def __init__(self, msg: str):
        self.message = msg

    def __str__(self):
        return f"TableConfigError: '{self.message}'"


if __name__ == '__main__':
    a = "/bbb///"
