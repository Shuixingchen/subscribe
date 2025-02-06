import scrapy
import logging
import traceback
from scrapy_selenium import SeleniumRequest
from selenium.webdriver import ActionChains
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import os
from twitter.funcs import get_cookies_file
from twitter.gptapi import GPTAPI
import twitter.db as db

class ReplySpider(scrapy.Spider):
    name = "reply"
    allowed_domains = ["x.com"]
    start_urls = ["https://x.com"]

    def start_requests(self):
        self.db = db.Db()
        uid = self.db.get_user_id()
        print("do reply uid: ", uid)
        
        url = "https://x.com"
        file_path = get_cookies_file(uid)
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                cookies = json.load(file)
            self.cookies = [{'key':cookie['name'], 'value':cookie['value']} for cookie in cookies]
        else:
            print("Error: ", "No cookies found")
            return
        yield SeleniumRequest(url=url, callback=self.do_post_reply)


    def do_post_reply(self, response):  
        reply_list = self.db.get_reply_list()
        for reply in reply_list:
            if reply['user_name'] == "":
                continue
            origin_post_url = self.post_replay(response,reply)
            if origin_post_url == "":
                continue
            reply['origin_post_url'] = origin_post_url
            self.db.save_reply_log(reply)
    def post_replay(self, response, reply):
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
            reply_content = GPTAPI().get_cn_response(article_content)
            print("reply user: ", reply['user_name'])
            print("reply content: ", reply_content)
            # 鼠标移动到文章上面
            actions.move_to_element(article).perform()
            time.sleep(1)
            article.click()
            time.sleep(3)
            last_url = driver.current_url
            print("Current URL after click: ", driver.current_url)

            # 获取富文本编辑框
            tweet_inputs = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[data-testid="tweetTextarea_0"]')))
            tweet_input = tweet_inputs[0]
            # 模拟键盘输入数据
            tweet_input.click()
            tweet_input.send_keys(reply_content)
            # reply 按钮
            reply_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-testid="tweetButtonInline"]')))
            # 将鼠标移动到元素
            actions.move_to_element(reply_button).perform()
            time.sleep(1)
            reply_button.click()
            time.sleep(3)
            return last_url
        except:
            logging.error(traceback.format_exc())
            return ""


    
