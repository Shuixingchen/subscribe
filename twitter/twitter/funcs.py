import requests
import json
import logging
import random
import time
def get_cookies_file(uid:int):
    return f"cookies/{uid}.json"

def rand_time_wait_second():
    time.sleep(random.randint(1, 60))
def rand_time_wait_minute():
    time.sleep(random.randint(1, 10)*60)
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