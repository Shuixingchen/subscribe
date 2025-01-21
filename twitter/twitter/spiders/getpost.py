import scrapy
from scrapy_selenium import SeleniumRequest
import logging
import traceback
from selenium.webdriver import ActionChains
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import twitter.db as db
import json
import os
from twitter.funcs import get_cookies_file
from twitter.gptapi import GPTAPI
from twitter.funcs import send_notice


class GetpostSpider(scrapy.Spider):
    name = "getpost"
    allowed_domains = ["x.com"]
    start_urls = ["https://x.com"]

    def start_requests(self):
        try:
            self.db = db.Db()
            uid = self.db.get_user_id()
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
        except:
            logging.error("Error: start_requests")
            logging.error(traceback.format_exc())
            return
        yield SeleniumRequest(url=url, callback=self.get_post)
    def get_post(self,response):
        try:
            users = self.db.get_big_user()
            for user in users:
                if user['username'] == "":
                    continue
                self.parse(response,user)
        except:
            logging.error(traceback.format_exc())
            return ""
    def parse(self, response,user):
        try:
            driver = response.request.meta["driver"]
            # 跳到大v主页
            driver.get("https://x.com/"+user['username'])
            wait = WebDriverWait(driver, 60)  # 设置最大等待时间为10秒
            actions = ActionChains(driver)
            # 滚动页面
            ActionChains(driver) \
            .scroll_by_amount(0, 200) \
            .perform()
            articles = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[data-testid="tweetText"]')))
            if len(articles) == 0:
                print("Error: ", "No articles found")
                return ""
            social_pinneds = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[data-testid="socialContext"]')))
            social_reposted = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'span[data-testid="socialContext"]')))
            socials = social_pinneds + social_reposted
            headers = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[data-testid="User-Name"]')))
            post_headers = []
            for i,header in enumerate(headers):
                try:
                    a_tag = header.find_element(By.CSS_SELECTOR, 'a[dir="ltr"][role="link"]')
                    post_headers.append({
                        "href": a_tag.get_attribute('href'),
                        "time": a_tag.get_attribute('aria-label')
                    })
                except Exception as e:
                    continue
            for index, article in enumerate(articles):
                if index < len(socials):
                    social = socials[index]
                    # print("index:",index,"social: ", social.text)
                if index < len(post_headers):
                    post_header = post_headers[index]
                    # print("index:",index,"post_header: ", post_header)
                # print("index:",index,"articles: ", article.text)
                data = {
                    "username": user['username'],
                    "article": article.text,
                    "post_id": post_header['href'] if index < len(post_headers) else "",
                    "social": social.text if index < len(socials) else "",
                    "post_time": post_header["time"] if index < len(post_headers) else "",
                }
                if data["post_id"] == "":
                    continue
                print("data: ", data)
                res = self.db.save_big_user_post(data)
                if res:
                    self.send_notice("twitter", data)
        except:
            logging.error(traceback.format_exc())
            return ""
    def send_notice(self,title,data):
         # 构造消息内容
        msg_lines = [title]
        for key, value in data.items():
            msg_lines.append(f"{key} = {value}")
        
        # 将所有行连接成一个字符串，并确保最后没有多余的换行符
        msg = '\n'.join(msg_lines)
        send_notice("https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=564f2499-fee1-42a0-8efb-7d9b65d33570", msg)