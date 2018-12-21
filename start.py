#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Miller"
# Date: 2018/12/21


import os

from config import Config

# 从容器环境变量更新配置
Config.LOCAL_REDIS["address"] = os.environ.get("REDIS_ADDR")
Config.SESSION_EXPIRES["db"] = int(os.environ.get("REDIS_EXPIRES"))

Config.DB_BI_CONFIG["host"] = os.environ.get("MYSQL_HOST")
Config.DB_BI_CONFIG["port"] = int(os.environ.get("MYSQL_PORT"))
Config.DB_BI_CONFIG["user"] = os.environ.get("MYSQL_USER")
Config.DB_BI_CONFIG["password"] = os.environ.get("MYSQL_PWD")
Config.DB_BI_CONFIG["db"] = os.environ.get("MYSQL_DB")
#

# 默认配置
from curd.control import AdminConfig

# 使用jinja2的模版, 必须在调用到curd.response之前修改
AdminConfig.Template = "jinja2"
# 增加模板路径
AdminConfig.add_template_path("./templates")
# 使用curd数据库对象和log对象
AdminConfig.MySQLDBConnParams = Config.DB_BI_CONFIG
AdminConfig.Listener = True

# 配置rbac认证
from rbac.control import RbacConfig

RbacConfig(AdminConfig)

# 注册表结构
import model
from curd.admin import init

from sanic import Sanic

app = Sanic(log_config=LOGGING_CONFIG_DEFAULTS)

# 初始化app的curd蓝图
init(app=app)

for k, v in app.router.routes_all.items():
    print(k, " -----------> ", v.handler.__name__, " -----------> ", v.methods, "--------->", v.name)
app.run(host="0.0.0.0", port=8000)





