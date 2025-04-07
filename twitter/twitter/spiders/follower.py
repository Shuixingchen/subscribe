import scrapy
from scrapy_selenium import SeleniumRequest
from selenium.webdriver import ActionChains
import time
import os
import logging
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from twitter.funcs import get_cookies_file
import twitter.db as db
from collections import deque

# 获取用户粉丝爬虫，只能获取最新的50条数据
class FollowerSpider(scrapy.Spider):
    name = "follower"
    allowed_domains = ["x.com","sannysoft.com"]
    start_urls = ["https://x.com/runtoweb3/verified_followers",
                  "https://x.com/runtoweb3/following",
                  "https://x.com/runtoweb3/followers"
                ]
    quenue = deque()

    def start_requests(self):
        self.db = db.Db()
        x_uid = os.getenv(self.name.upper()+'_USER_ID')
        if x_uid is None:
            uid = self.db.get_user_id()
        else:
            uid = int(x_uid)
        print("do post uid: ", uid)
    
        url = "https://x.com/home"
        file_path = get_cookies_file(uid)
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                cookies = json.load(file)
            self.cookies = [{'key':cookie['name'], 'value':cookie['value']} for cookie in cookies]
        else:
            logging.info("cookies not found")
            return
        yield SeleniumRequest(url=url, callback=self.parse)

    def parse(self, response):
       self.db.get_big_user()
       while True:
            if len(self.quenue) == 0:
                self.quenue.extend(self.start_urls)
            url = self.quenue.popleft()
       
    def get_follower(self, response):
        driver = response.request.meta["driver"]
        follows = []
        # 给浏览器添加Cookie
        for item in self.cookies:
            driver.add_cookie({'name': item['key'], 'value': item['value']})
        driver.get(self.start_urls[2])
        wait = WebDriverWait(driver, 10)  # 设置最大等待时间为10秒
        elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[data-testid="cellInnerDiv"]')))
        for f in elements:
            try:
                aElements = f.find_element(By.CSS_SELECTOR, "a")
                url = aElements.get_attribute('href')
                print(url)
                name = url.split("/")[-1]
                follows.append(name)
            except Exception as e:
                break
        # 鼠标滚动，屏幕1920x1080,滚动三维之一屏
        ActionChains(driver) \
            .scroll_by_amount(0, 300) \
            .perform()
        unique_list = list(dict.fromkeys(follows))