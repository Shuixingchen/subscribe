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
    db = db.Db()
    def start_requests(self):
        x_uid = os.getenv(self.name.upper()+'_USER_ID')
        if x_uid is None:
            uid = self.db.get_user_id()
        else:
            uid = int(x_uid)
        print("test uid ", uid)
        # yield SeleniumRequest(url=self.start_urls[0], callback=self.do_login)
    def parse(self, response):
        print("parse")
        time.sleep(10)

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