#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Miller"
# Date: 2018/12/12


import asyncio
import aiomysql

from curd.interface import IBehaviorLog
class TestDB(IBehaviorLog):
    # def __init__(self):
    #     self.init()

    def init(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.pool = self.loop.run_until_complete(aiomysql.create_pool(host='127.0.0.1', port=3306,
                                                                      user='root', password='woaichenni',
                                                                      db='miller_blogs', loop=self.loop))

    async def select(self, sql, *args):
        sql = sql % tuple(args) if args else sql

        async with (await  self.pool.acquire()) as conn:
            async with conn.cursor() as cur:
                await cur.execute(sql)
                r = await cur.fetchall()
        return r

    def test_select(self, sql, *args):
        sql = 'select * from role'
        rs = self.loop.run_until_complete(self.select(sql))
        print(rs)

    # def test_insert(self):
    #     sql = 'insert into `minifw` (`name`) values (?)'
    #     rs = self.loop.run_until_complete(base_db.insert(self.pool, sql, args=('test_val',)))
    #     self.assertEqual(rs, 1)

    def tearDown(self):
        self.loop.close()
        del self.loop


if __name__ == '__main__':
    a = TestDB()
    a.test_select("select * from role")
    a.test_select("select * from role")
    a.test_select("select * from role")
    a.test_select("select * from role")
    a.test_select("select * from role")
