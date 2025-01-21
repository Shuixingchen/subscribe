import requests
import json
import logging
def get_cookies_file(uid:int):
    return f"cookies/{uid}.json"

def send_notice(url,content:str):
    if not url or not content:
        return
    # 定义消息体
    payload = {
        "msgtype": "text",
        "text": {
            "content": content
        }
    }
    try:
        # 发送POST请求
        response = requests.post(
            url,
            headers={'Content-Type': 'application/json'},
            data=json.dumps(payload)
        )
        logging.info(f"send notice success:{response.text}")
    except:
        logging.error(f"send notice error:")