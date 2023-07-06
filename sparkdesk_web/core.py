# -*- coding: UTF-8 -*-
"""
@Project : sparkdesk-api
@File    : core.py
@Author  : HildaM
@Email   : Hilda_quan@163.com
@Date    : 2023/7/6 15:00
@Description : web接口核心入口
"""
import json
import sys

import requests

from sparkdesk_web.utils import decode, load_session_log, save_session_log
from sparkdesk_web.web import create_header


class SparkWeb:
    cookie = ""
    fd = ""
    GtToken = ""
    header = ""
    chat_id = ""

    def __init__(self, cookie, fd, GtToken):
        self.cookie = cookie
        self.fd = fd
        self.GtToken = GtToken

        self.header = create_header(cookie)

    def generate_chat_id(self):
        url = 'https://xinghuo.xfyun.cn/iflygpt/u/chat-list/v1/create-chat-list'
        payload = "{}"
        response = requests.request("POST", url, headers=self.header, data=payload)
        response_data = json.loads(response.text)
        if response_data['code'] == 0:
            chat_list_id = response_data['data']['id']
            return chat_list_id
        else:
            return '0'

    def set_name(self, question):
        url = "https://xinghuo.xfyun.cn/iflygpt/u/chat-list/v1/rename-chat-list"
        question = question[:15]
        payload = {
            'chatListId': self.chat_id,
            'chatListName': question,
        }
        response = requests.request("POST", url, headers=self.header, data=json.dumps(payload))
        response_data = json.loads(response.text)
        if response_data['code'] != 0:
            print('\nFailed to initialize session name.')

    def chat(self, question):
        url = "https://xinghuo.xfyun.cn/iflygpt-chat/u/chat_message/chat"
        payload = {
            'fd': self.fd,
            'chatId': self.chat_id,
            'text': question,
            'GtToken': self.GtToken,
            'clientType': '1'
        }
        response = requests.request("POST", url, headers=self.header, data=payload, stream=True)
        response_text = ''
        for line in response.iter_lines():
            if line:
                encoded_data = line[len("data:"):]
                missing_padding = len(encoded_data) % 4
                if missing_padding != 0:
                    encoded_data += b'=' * (4 - missing_padding)
                if decode(encoded_data) != 'zw':
                    sys.stdout.flush()
                    answer = decode(encoded_data).replace('\n\n', '\n')
                    response_text += answer

        return response_text

    def chat_stream(self):
        try:
            # Load session log, and read directly if it exists.
            log_exist, chat_id = load_session_log()
            if log_exist is False:
                is_new_session = True
                self.chat_id = self.generate_chat_id()
                self.set_name("New converation")
            else:
                # 提示是否载入上次的会话
                while True:
                    answer = input("是否载入上次的会话？(Y/N): ")
                    if answer.upper() == "Y":
                        is_new_session = False
                        self.chat_id = chat_id
                        break
                    elif answer.upper() == "N":
                        is_new_session = True
                        self.chat_id = self.generate_chat_id()  # 生成新的会话ID
                        break
                    else:
                        print("请输入正确的选项！")

            count = 0
            print(
                '您好，我是科大讯飞研发的认知智能大模型，我的名字叫讯飞星火认知大模型。我可以和人类进行自然交流，解答问题，高效完成各领域认知智能需求。')
            while True:
                count += 1
                question = input("\n请输入您的问题：")
                if question == 'exit':
                    break
                resp = self.chat(question)
                print("\nSparkDesk_AI: " + resp)
                if is_new_session == True & count == 1:
                    self.set_name(question)  # 设置会话名称
            # 保存会话日志
            save_session_log(self.chat_id)

        except KeyboardInterrupt:
            # 保存会话日志并退出程序
            save_session_log(self.chat_id)

        print("\n感谢您使用讯飞星火认知大模型，欢迎再次使用！")
