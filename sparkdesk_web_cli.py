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
from pyhandytools.file import FileUtils

if __name__ == '__main__':
    conf_data = FileUtils.load_json('./conf/keys.json')

    sparkWeb = SparkWeb(
        cookie=conf_data['Cookie'],
        fd=conf_data['fd'],
        GtToken=conf_data['GtToken']
    )

    # single chat
    # print(sparkWeb.chat("repeat: hello world"))

    # stream input chat
    #sparkWeb.chat_stream(history=True)

    # continue chat
    chat = sparkWeb.create_continuous_chat()
    print(chat.chat("请介绍一下西安"))
    print(chat.chat("刚才你说的是哪个城市？"))