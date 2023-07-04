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


class SparkAPI:
    api_url = 'ws(s)://spark-api.xf-yun.com/v1.1/chat'
    max_token = 2048

    def __init__(self, app_id, api_key, api_secret, max_token):
        self.app_id = app_id
        self.api_key = api_key
        self.api_secret = api_secret
        self.max_token = max_token

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

    @staticmethod
    def get_prompt(query: str, history: list):
        use_message = {"role": "user", "content": query}
        history.append(use_message)
        message = {"text": history}
        return message

    @staticmethod
    def process_response(response_str: str, history: list):
        res_dict: dict = json.loads(response_str)
        code = res_dict.get("header", {}).get("code")
        status = res_dict.get("header", {}).get("status", 2)

        if code == 0:
            res_dict = res_dict.get("payload", {}).get("choices", {}).get("text", [{}])[0]
            res_content = res_dict.get("content", "")

            if len(res_dict) > 0 and len(res_content) > 0:
                if "index" in res_dict:
                    del res_dict["index"]
                response = res_content

                if status == 0:
                    history.append(res_dict)
                else:
                    # In continuous result generation, add the newly returned content to the response.
                    history[-1]["content"] += response
                    response = history[-1]["content"]

                return response, history, status
            else:
                return "", history, status
        else:
            print("error code ", code)
            print("you can see this website to know code detail")
            print("https://www.xfyun.cn/doc/spark/%E6%8E%A5%E5%8F%A3%E8%AF%B4%E6%98%8E.html")
            return "", history, status

    def chat_stream(
            self,
            query: str,
            history: list,
            user_id: str = "001",
            domain: str = "general",
            max_tokens: int = 2048,
            temperature: float = 0.5,
    ):
        # the max of max_length is 4096
        max_tokens = min(max_tokens, 4096)
        url = self.get_authorization_url()
        ws = create_connection(url)

        message = self.get_prompt(query, history)
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
                response, history, status = self.process_response(
                    response_str, history
                )
                yield response, history

                """
                The final return result, which means a complete conversation.
                doc url: https://www.xfyun.cn/doc/spark/Web.html#_1-%E6%8E%A5%E5%8F%A3%E8%AF%B4%E6%98%8E
                """
                if len(response) == 0 or status == 2:
                    break
                response_str = ws.recv()

        except WebSocketConnectionClosedException:
            print("Connection closed")
        finally:
            ws.close()
