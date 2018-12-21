#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Miller"
# Date: 2018/12/18
import hashlib


def md5_check(value, binary=False, leftsalt="", rightsalt=""):
    """
    单个值或多个值进行md5校验
    :param value: 字符串列表或独立字符串
    :param binary: 二进制校验
    :param leftsalt: 左加盐
    :param rightsalt: 右加盐
    :return:
    """
    md5 = hashlib.md5()
    if isinstance(value, str):
        value = leftsalt + value + rightsalt

        if not binary:
            value = value.encode(encoding='utf_8')
        md5.update(value)

    elif isinstance(value, (list, tuple)):
        for val in value:
            if not isinstance(val, str):
                val = str(val)
            val = leftsalt + val + rightsalt

            if not binary:
                val = val.encode(encoding='utf_8')
            md5.update(val)
    return md5.hexdigest()


if __name__ == '__main__':
    print(md5_check("xxxxxxxx", leftsalt="aa", rightsalt="bb"))
    print(md5_check(["xxxxxxxx"], leftsalt="aa", rightsalt="bb"))
