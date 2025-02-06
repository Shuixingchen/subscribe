import scrapy
from scrapy_selenium import SeleniumRequest
from twitter.gptapi import GPTAPI
import twitter.db as db
import time
from twitter.funcs import get_cookies_file
import os
import json


class TestSpider(scrapy.Spider):
    name = "test"
    allowed_domains = ["x.com"]
    start_urls = ["https://x.com"]

    def start_requests(self):
        self.db = db.Db()
        uid = self.db.get_user_id()
        print("do reply uid: ", uid)

        # message = """
        # 有谁知道最近哪些meme币比较有前景啊？
        # """
        # res = GPTAPI().get_cn_response(message)
        # print(res)
        # return
        yield SeleniumRequest(url=self.start_urls[0], callback=self.do_login)
    def parse(self, response):
        print("parse")
        time.sleep(300)

    def do_login(self, response):
        driver = response.request.meta["driver"]
        uid = self.db.get_user_id()
        file_path = get_cookies_file(uid)
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                cookies = json.load(file)
            self.cookies = [{'key':cookie['name'], 'value':cookie['value']} for cookie in cookies]
         # 给浏览器添加Cookie
        if hasattr(self, 'cookies'):
            for item in self.cookies:
                driver.add_cookie({'name': item['key'], 'value': item['value']})
            time.sleep(5)
        time.sleep(300)