# -*- coding: UTF-8 -*-
"""
@Project : sparkdesk-api
@File    : core.py
@Author  : HildaM
@Email   : Hilda_quan@163.com
@Date    : 2023/7/4 16:50
@Description : The core entry point of the API interface
"""
import base64
import hmac
import json
from datetime import datetime, timezone
from urllib.parse import urlencode, urlparse
from websocket import create_connection, WebSocketConnectionClosedException
from sparkdesk_api.utils import get_prompt, process_response


class SparkAPI:
    api_url = 'wss://spark-api.xf-yun.com/v1.1/chat'
    max_token = 2048

    def __init__(self, app_id, api_key, api_secret):
        self.app_id = app_id
        self.api_key = api_key
        self.api_secret = api_secret

    def set_max_tokens(self, token):
        if isinstance(token, int) is False or token < 0:
            print("set_max_tokens() error: tokens should be a positive integer!")
            return
        self.max_token = token

    """
    doc url: https://www.xfyun.cn/doc/spark/general_url_authentication.html
    """

    def get_authorization_url(self):
        authorize_url = urlparse(self.api_url)
        # 1. generate data
        date = datetime.now(timezone.utc).strftime('%a, %d %b %Y %H:%M:%S %Z')

        """
        Generation rule of Authorization parameters
            1) Obtain the APIKey and APISecret parameters from the console.
            2) Use the aforementioned date to dynamically concatenate a string tmp. Here we take Huobi's URL as an example, 
                the actual usage requires replacing the host and path with the specific request URL.
        """
        signature_origin = "host: {}\ndate: {}\nGET {} HTTP/1.1".format(
            authorize_url.netloc, date, authorize_url.path
        )
        signature = base64.b64encode(
            hmac.new(
                self.api_secret.encode(),
                signature_origin.encode(),
                digestmod='sha256'
            ).digest()
        ).decode()
        authorization_origin = \
            'api_key="{}",algorithm="{}",headers="{}",signature="{}"'.format(
                self.api_key, "hmac-sha256", "host date request-line", signature
            )
        authorization = base64.b64encode(authorization_origin.encode()).decode()
        params = {
            "authorization": authorization,
            "date": date,
            "host": authorize_url.netloc
        }

        ws_url = self.api_url + "?" + urlencode(params)
        return ws_url

    def build_inputs(
            self,
            message: dict,
            user_id: str = "001",
            domain: str = "general",
            temperature: float = 0.5,
            max_tokens: int = 2048
    ):
        input_dict = {
            "header": {
                "app_id": self.app_id,
                "uid": user_id,
            },
            "parameter": {
                "chat": {
                    "domain": domain,
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                }
            },
            "payload": {
                "message": message
            }
        }
        return json.dumps(input_dict)

    def chat(
            self,
            query: str,
            history: list = None,  # store the conversation history
            user_id: str = "001",
            domain: str = "general",
            max_tokens: int = 2048,
            temperature: float = 0.5,
    ):
        if history is None:
            history = []

        # the max of max_length is 4096
        max_tokens = min(max_tokens, 4096)
        url = self.get_authorization_url()
        ws = create_connection(url)
        message = get_prompt(query, history)
        input_str = self.build_inputs(
            message=message,
            user_id=user_id,
            domain=domain,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        ws.send(input_str)
        response_str = ws.recv()
        try:
            while True:
                response, history, status = process_response(response_str, history)
                """
                The final return result, which means a complete conversation.
                doc url: https://www.xfyun.cn/doc/spark/Web.html#_1-%E6%8E%A5%E5%8F%A3%E8%AF%B4%E6%98%8E
                """
                if len(response) == 0 or status == 2:
                    break
                response_str = ws.recv()
            return response

        except WebSocketConnectionClosedException:
            print("Connection closed")
        finally:
            ws.close()

    # Stream output statement, used for terminal chat.
    def chat_stream(
            self,
            query: str,
            history: list = None,  # store the conversation history
            user_id: str = "001",
            domain: str = "general",
            max_tokens: int = 2048,
            temperature: float = 0.5,
    ):
        if history is None:
            history = []

        # the max of max_length is 4096
        max_tokens = min(max_tokens, 4096)
        url = self.get_authorization_url()
        ws = create_connection(url)

        message = get_prompt(query, history)
        input_str = self.build_inputs(
            message=message,
            user_id=user_id,
            domain=domain,
            temperature=temperature,
            max_tokens=max_tokens,
        )

        # send question or prompt to url, and receive the answer
        ws.send(input_str)
        response_str = ws.recv()

        # Continuous conversation
        try:
            while True:
                response, history, status = process_response(response_str, history)
                yield response, history
                if len(response) == 0 or status == 2:
                    break
                response_str = ws.recv()

        except WebSocketConnectionClosedException:
            print("Connection closed")
        finally:
            ws.close()
