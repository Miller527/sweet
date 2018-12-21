#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Miller"
# Date: 2018/12/13


from curd.interface import IBehaviorLog


class ElasticSearchDB(IBehaviorLog):
    def init(self):
        pass

    def write(self, data: dict):
        pass

    def close(self):
        pass


es = ElasticSearchDB()
