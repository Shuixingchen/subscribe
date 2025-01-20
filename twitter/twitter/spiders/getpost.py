import scrapy
from scrapy_selenium import SeleniumRequest
import logging
import traceback
from selenium.webdriver import ActionChains
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pymysql
import json
import os
from twitter.funcs import get_cookies_file
from twitter.gptapi import GPTAPI


class GetpostSpider(scrapy.Spider):
    name = "getpost"
    allowed_domains = ["x.com"]
    start_urls = ["https://x.com"]

    def start_requests(self):
        self.mysql_init()
        uid = self.get_user_id()
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
    def parse(self, response,reply):
        try:
            driver = response.request.meta["driver"]
            # 给浏览器添加Cookie
            if hasattr(self, 'cookies'):
                for item in self.cookies:
                    driver.add_cookie({'name': item['key'], 'value': item['value']})
                time.sleep(5)
            
            # 跳到大v主页
            driver.get("https://x.com/"+reply['user_name'])
            wait = WebDriverWait(driver, 60)  # 设置最大等待时间为10秒
            actions = ActionChains(driver)
            articles = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[data-testid="tweetText"]')))
            if len(articles) == 0:
                print("Error: ", "No articles found")
                return ""
            article = articles[0]
            article_content = article.text
            print("article: ", article_content)
            if len(article_content) < 10:
                print("Error: ", "No article content found")
                return ""
            # 鼠标移动到文章上面
            actions.move_to_element(article).perform()
            time.sleep(1)
            article.click()
            time.sleep(3)
            last_url = driver.current_url
            print("Current URL after click: ", last_url)
            return last_url
        except:
            logging.error(traceback.format_exc())
            return ""