# -*- coding: UTF-8 -*-
"""
@Project : sparkdesk-api
@File    : sparkdesk_web_cli.py
@Author  : HildaM
@Email   : Hilda_quan@163.com
@Date    : 2023/7/6 19:07
@Description : 
"""
from sparkdesk_web.core import SparkWeb

if __name__ == '__main__':
    cookie = input("cookie: ")
    fd = input("fd: ")
    GtToken = input("GtToken: ")

    sparkWeb = SparkWeb(
        cookie=cookie,
        fd=fd,
        GtToken=GtToken
    )

    # single chat
    # print(sparkWeb.chat("repeat: hello world"))

    # continue chat
    sparkWeb.chat_stream()