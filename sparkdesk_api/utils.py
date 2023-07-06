# -*- coding: UTF-8 -*-
"""
@Project : sparkdesk-api
@File    : utils.py
@Author  : HildaM
@Email   : Hilda_quan@163.com
@Date    : 2023/7/4 20:09
@Description : chat utils
"""
import json


def get_prompt(query: str, history: list):
    use_message = {"role": "user", "content": query}
    if history is None:
        history = []
    history.append(use_message)
    message = {"text": history}
    return message



"""
param reference:
    status:
        Text response status, with values of [0, 1, 2]; 
        0 represents the first text result, 1 represents intermediate text results, and 2 represents the last text result.

"""
def process_response(response_str: str, history: list):
    res_dict: dict = json.loads(response_str)
    code = res_dict.get("header", {}).get("code")
    status = res_dict.get("header", {}).get("status", 2)

    if code == 0:
        res_dict = res_dict.get("payload", {}).get("choices", {}).get("text", [{}])[0]
        res_content = res_dict.get("content", "")

        if len(res_dict) > 0 and len(res_content) > 0:
            # Ignore the unnecessary data
            if "index" in res_dict:
                del res_dict["index"]
            response = res_content

            if status == 0:
                history.append(res_dict)
            else:
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
