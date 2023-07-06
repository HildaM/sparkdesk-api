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
from sparkdesk_web.web import create_chat_header, create_request_header


class SparkWeb:
    __cookie = ""
    __fd = ""
    __GtToken = ""
    __chat_id = ""
    __chat_header = ""
    __request_header = ""

    def __init__(self, cookie, fd, GtToken):
        self.__cookie = cookie
        self.__fd = fd
        self.__GtToken = GtToken
        self.__cha_header = create_chat_header(cookie)
        self.__request_header = create_request_header(cookie)

    def __generate_chat_id(self):
        url = 'https://xinghuo.xfyun.cn/iflygpt/u/chat-list/v1/create-chat-list'
        payload = "{}"
        response = requests.request("POST", url, headers=self.__request_header, data=payload)
        response_data = json.loads(response.text)
        if response_data['code'] == 0:
            chat_list_id = response_data['data']['id']
            return chat_list_id
        else:
            return '0'

    def __set_name(self, question):
        url = "https://xinghuo.xfyun.cn/iflygpt/u/chat-list/v1/rename-chat-list"
        question = question[:15]
        payload = {
            'chatListId': self.__chat_id,
            'chatListName': question,
        }
        response = requests.request("POST", url, headers=self.__request_header, data=json.dumps(payload))
        response_data = json.loads(response.text)
        if response_data['code'] != 0:
            print('\nFailed to initialize session name.')

    def __get_resp(self, question):
        url = "https://xinghuo.xfyun.cn/iflygpt-chat/u/chat_message/chat"
        payload = {
            'fd': self.__fd,
            'chatId': self.__chat_id,
            'text': question,
            'GtToken': self.__GtToken,
            'clientType': '1'
        }
        response = requests.request("POST", url, headers=self.__cha_header, data=payload, stream=True)
        return response

    def chat(self, question):
        self.__chat_id = self.__generate_chat_id()
        self.__set_name("SparkDesk AI chat")

        response = self.__get_resp(question)
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

    def __streaming_output(self, question):
        response = self.__get_resp(question)
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
                    print(answer, end="")
        print("\n")

    def chat_stream(self):
        try:
            self.__chat_id = self.__generate_chat_id()
            self.__set_name("SparkDesk AI chat")
            print("Enter exit or stop to end the converation.\n")
            count = 0
            while True:
                count += 1
                question = input("Ask: ")
                if question == 'exit' or question == 'stop':
                    break
                self.__streaming_output(question)

        finally:
            print("\nThank you for using the SparkDesk AI. Welcome to use it again!")

