# -*- coding: UTF-8 -*-
"""
@Project : sparkdesk-api
@File    : sparkdesk_api_cli.py
@Author  : HildaM
@Email   : Hilda_quan@163.com
@Date    : 2023/7/6 18:56
@Description : 
"""
from sparkdesk_api.core import SparkAPI

if __name__ == '__main__':
    app_id = input("app_id: ")
    api_secret = input("api_secret: ")
    api_key = input("api_key: ")

    sparkAPI = SparkAPI(
        app_id=app_id,
        api_secret=api_secret,
        api_key=api_key
    )

    # single chat
    # print(sparkAPI.chat("repeat: hello world"))

    # continue chat
    sparkAPI.chat_stream()