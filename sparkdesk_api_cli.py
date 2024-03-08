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

    # 默认api接口版本为1.5，2.0需要自行申请。开启v2.0版本只需指定 version=2.1 即可
    sparkAPI = SparkAPI(
        app_id=app_id,
        api_secret=api_secret,
        api_key=api_key,
        # version=2.1
        # assistant_id="xyzspsb4i5s7_v1"
    )

    # single chat
    # print(sparkAPI.chat("repeat: hello world"))

    # continue chat
    sparkAPI.chat_stream()