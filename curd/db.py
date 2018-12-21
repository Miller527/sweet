#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Miller"
# Date: 2018/12/12

import asyncio
import aiomysql

from curd.interface import IBehaviorLog


class MySQLDB(IBehaviorLog):

    def init(self):
        self.pool = self.kwargs.get("pool")
        # self.loop = self.kwargs.get("loop")
        # # dir("looppppppp", self.loop)
        # print(dir(self.loop), len(dir(self.loop)))
        # # if not self.loop:
        # #     raise "x"
        #
        # # asyncio.set_event_loop(self.loop)
        # print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",self.loop)
        # #         self.pool = self.loop.run_until_complete(aiomysql.create_pool(host='127.0.0.1', port=3306,
        # #                                                                       user='root', password='woaichenni',
        # #                                                                       db='miller_blogs', loop=self.loop))
        # print(        self.loop.is_running())
        # print(        self.loop.stop())
        # print(        self.loop.is_running())
        # self.pool = self.loop.run_in_executor(aiomysql.create_pool(host='127.0.0.1', port=3306,
        #                                                               user='root', password='woaichenni',
        #                                                               db='miller_blogs', loop=self.loop))
        # print("xxxxxxx", dir(self.pool), type(self.pool))

    async def _select(self, sql,**kwargs):
        async with (await self.pool.acquire()) as conn:
            async with conn.cursor() as cur:
                await cur.execute(sql)
                if kwargs.get("fetchone") is True:
                    r = await cur.fetchone()
                else:
                    r = await cur.fetchall()
        return r

    async def _insert(self, sql):
        async with (await self.pool.acquire()) as conn:
            async with conn.cursor() as cur:
                res = await cur.execute(sql)
                await conn.commit()
        return res

    def select(self, sql, *args,**kwargs):

        sql = sql % tuple(args) if args else sql
        return self._select(sql,**kwargs)

    def insert(self, sql, *args):
        sql = self.join_sql(sql, *args)
        res = self._insert(sql)
        return res

    @staticmethod
    def join_sql(sql, *args):
        return sql % tuple(args) if args else sql

    def close(self):
        self.loop.close()
        del self.loop

    def write(self, data: dict):
        pass



#
# import asyncio
# import aiomysql
#
#
# class TestDB(object):
#     async def _select(self, sql):
#         print(dir(self.pool))
#         async with (await   self.pool.acquire() )as conn:
#             async with conn.cursor() as cur:
#                 await cur.execute(sql)
#                 r = await cur.fetchall()
#                 print(r)
#
#     def __init__(self):
#         self.loop = asyncio.new_event_loop()
#         print(dir(self.loop),len(dir(self.loop)))
#         asyncio.set_event_loop(self.loop)
#
#         print("xxxxxxxxxxxxx")
#         print(dir(self.loop),len(dir(self.loop)))
#         print(self.loop.is_running())
#         self.pool = self.loop.run_until_complete(aiomysql.create_pool(host='127.0.0.1', port=3306,
#                                                                       user='root', password='woaichenni',
#                                                                       db='miller_blogs', loop=self.loop))
#
#         # print(dir(self.pool))
#         # print(dir(aiomysql.create_pool(host='127.0.0.1', port=3306,
#         #                                                               user='root', password='woaichenni',
#         #                                                               db='miller_blogs', loop=self.loop)))
#     def test_select(self):
#         sql = 'select * from role '
#         rs = self.loop.run_until_complete(self._select(sql))
#         print(rs)
#     def tearDown(self):
#         self.loop.close()
#         del self.loop
#
# if __name__ == '__main__':
#     x = TestDB()
#     x.test_select()
