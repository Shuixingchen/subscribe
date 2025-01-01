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

# 获取用户粉丝爬虫，只能获取最新的50条数据
class PostSpider(scrapy.Spider):
    name = "post"
    allowed_domains = ["x.com","sannysoft.com"]
    start_urls = ["https://x.com/home","https://x.com"]
    def start_requests(self):
        self.mysql_init()
        uid = self.get_user_id()
        print("do post uid: ", uid)
    
        url = "https://x.com"
        file_path = get_cookies_file(uid)
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                cookies = json.load(file)
            self.cookies = [{'key':cookie['name'], 'value':cookie['value']} for cookie in cookies]
        
        yield SeleniumRequest(url=url, callback=self.send_post)


    def send_post(self, response):
        try:
            driver = response.request.meta["driver"]
            # 给浏览器添加Cookie
            if hasattr(self, 'cookies'):
                for item in self.cookies:
                    driver.add_cookie({'name': item['key'], 'value': item['value']})
                time.sleep(5)
            
            driver.get(self.start_urls[0])
            wait = WebDriverWait(driver, 60)  # 设置最大等待时间为10秒
            # 聚焦富文本可编辑元素
            tweet_inputs = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[data-testid="tweetTextarea_0"]')))
            tweet_input = tweet_inputs[0]
        
            # 模拟键盘输入数据
            post_content = GPTAPI().get_random_content()
            print("post_content:", post_content)
            tweet_input.click()
            tweet_input.send_keys(post_content)
    
            time.sleep(5)
            actions = ActionChains(driver)
            # 获取post按钮
            tweet_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-testid="tweetButtonInline"]')))
            # 将鼠标移动到元素
            actions.move_to_element(tweet_button).perform()
            time.sleep(1)
            tweet_button.click()
            time.sleep(5)
        except:
            logging.error("send_post",traceback.format_exc())
       
    def do_login(self, response):
        x_email = self.crawler.settings.get('X_EMAIL')
        x_password = self.crawler.settings.get('X_PASSWORD')
        x_username = self.crawler.settings.get('X_USERNAME')
        driver = response.request.meta["driver"]
        wait = WebDriverWait(driver, 60)  # 设置最大等待时间为10秒

        # 找到登录用户名input
        email_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[autocomplete="username"]')))
        email_input.send_keys(x_email)

        # 点击下一步
        actions = ActionChains(driver)
        next_buttons = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'button[role="button"]')))
        next_button = next_buttons[3]
        actions.move_to_element(next_button).perform()
        time.sleep(1)
        next_button.click()

        # 输入用户名
        user_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[data-testid="ocfEnterTextTextInput"]')))
        user_input.send_keys(x_username)
        
        # 点击下一步
        next_buttons_2 = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'button[role="button"]')))
        # for i, button in enumerate(next_buttons_2):
        #     print(f"Button {i+1} HTML:")
        #     print(button.get_attribute('outerHTML'))
        next_button = next_buttons_2[2]
        actions.move_to_element(next_button).perform()
        time.sleep(1)
        next_button.click()

        # 输入密码
        password_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[name="password"]')))
        password_input.send_keys(x_password)

        # 点击登录
        login_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-testid="LoginForm_Login_Button"]')))
        actions.move_to_element(login_button).perform()
        login_button.click()

        # 等待页面 URL 发生变化，表示登录完成
        wait.until(EC.url_changes(driver.current_url))
        time.sleep(3)
        # 获取当前页面的所有 cookie
        cookies = driver.get_cookies()
        print("cookies:",cookies)
        self.save_cookies(cookies)
        time.sleep(10)

    def write_file(self, driver):
        html_source = driver.page_source
        with open('webpage.html', 'a', encoding='utf-8') as file:
                file.write(html_source)
    
    def save_cookies(self, cookies):
        # cookies = [{'domain': '.x.com', 'expiry': 1766215508, 'httpOnly': False, 'name': 'twid', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'u%3D1869988014640046080'}, {'domain': 'x.com', 'httpOnly': False, 'name': 'lang', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'en'}, {'domain': '.x.com', 'expiry': 1769239506, 'httpOnly': False, 'name': 'ct0', 'path': '/', 'sameSite': 'Lax', 'secure': True, 'value': '365a776e07757a3e38e8c15f037f9b9619f736f37f07fa48707e1e5492fa7c995d60866402b910e13c06c62ed3f55363f8c924050f455b538467705592872668598c9eb300e1931630c9063213278eda'}, {'domain': '.x.com', 'expiry': 1734765906, 'httpOnly': True, 'name': 'att', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': '1-MEsfpCtuxcJC8zV2cD2OS1P1H3WlD4aRGhX5w6ZE'}, {'domain': '.x.com', 'expiry': 1769239506, 'httpOnly': True, 'name': 'auth_token', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': '798ca81c9d2d09a098da7e4308acf968969fcf82'}, {'domain': '.x.com', 'expiry': 1766215508, 'httpOnly': False, 'name': 'personalization_id', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': '"v1_KBPOnz9E4KcPMsN2eyHIAQ=="'}, {'domain': '.x.com', 'expiry': 1769239506, 'httpOnly': True, 'name': 'kdt', 'path': '/', 'sameSite': 'Lax', 'secure': True, 'value': 'oxPJksv12hD9n5btUXuvNBA6DkpN7dtzxFV6nucu'}, {'domain': '.x.com', 'expiry': 1766215507, 'httpOnly': False, 'name': 'night_mode', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': '2'}, {'domain': '.x.com', 'expiry': 1769239508, 'httpOnly': False, 'name': 'guest_id_ads', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'v1%3A173467952393767084'}, {'domain': '.x.com', 'expiry': 1734688493, 'httpOnly': False, 'name': 'gt', 'path': '/', 'sameSite': 'Lax', 'secure': True, 'value': '1870007578304094359'}, {'domain': '.x.com', 'expiry': 1769239508, 'httpOnly': False, 'name': 'guest_id_marketing', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'v1%3A173467952393767084'}, {'domain': '.x.com', 'expiry': 1766215493, 'httpOnly': False, 'name': 'guest_id', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': '173467952393767084'}]
        with open('cookiefile.json', 'w') as file:  # 以文本模式打开文件
            json.dump(cookies, file, indent=4) 
    def save_header(self,response):
        headers_dict = dict(response.headers)
        print("heards",headers_dict)
        # 保存headers到json文件
        with open('headers.json', 'w') as file:
            json.dump(headers_dict, file, indent=4)

    def get_post_content(self,response):
        host = self.crawler.settings.get('X_MYSQL_HOST')
        user = self.crawler.settings.get('X_MYSQL_USER')
        password = self.crawler.settings.get('X_MYSQL_PASSWORD')
        database = self.crawler.settings.get('X_MYSQL_DATABASE')
        port = self.crawler.settings.get('X_MYSQL_PORT')
        self.conn = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=int(port),
            cursorclass=pymysql.cursors.DictCursor
        )
        self.cursor = self.conn.cursor()
        
    
    def get_user_id(self):
        try:
            query_user_id = """
            SELECT id from t_users where status = 1
            """
            self.cursor.execute(query_user_id,())
            user_id = self.cursor.fetchone()
            return user_id['id']
        except Exception as e:
            print("Error: ", e)
    def mysql_init(self):
        host = self.crawler.settings.get('X_MYSQL_HOST')
        user = self.crawler.settings.get('X_MYSQL_USER')
        password = self.crawler.settings.get('X_MYSQL_PASSWORD')
        database = self.crawler.settings.get('X_MYSQL_DATABASE')
        port = self.crawler.settings.get('X_MYSQL_PORT')
        self.conn = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=int(port),
            cursorclass=pymysql.cursors.DictCursor
        )
        self.cursor = self.conn.cursor()