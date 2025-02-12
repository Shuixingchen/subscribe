import scrapy
from scrapy_selenium import SeleniumRequest
from selenium.webdriver import ActionChains
import time
import logging
import traceback
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import os
from twitter.funcs import get_cookies_file
import twitter.db as db

class LoginSpider(scrapy.Spider):
    name = "login"
    allowed_domains = ["x.com"]
    start_urls = ["https://x.com"]

    def start_requests(self):
        self.db = db.Db()
        url = "https://x.com/i/flow/login"
        yield SeleniumRequest(url=url, callback=self.do_login)

    def parse(self, response):
        pass
    def do_login(self, response):
        user = self.db.get_user()
        print("do login uid: ", user['id'])
        cookiefile = get_cookies_file(user['id'])
        if os.path.exists(cookiefile):
            print(f"{user['username']} 已经登录")
            return
        res = self.x_login(response, user)
        if res:
            print(f"{user['username']} 登录成功")
        else:
            print(f"{user['username']} 登录失败")
    def x_login(self, response, user):
        try:
            x_email = user['email']
            x_password = user['password']
            x_username = user['username']
            uid = user['id']
            driver = response.request.meta["driver"]
            wait = WebDriverWait(driver, 10)  # 设置最大等待时间为10秒

            # 找到登录用户名input
            email_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[autocomplete="username"]')))
            email_input.send_keys(x_email)

            # 点击下一步
            actions = ActionChains(driver)
            next_buttons = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'button[role="button"]')))
            for i, button in enumerate(next_buttons):
                print(f"email Button {i+1} HTML:")
                print(button.text)
                if button.text == "Next" or button.text == "下一步":
                    next_button = button
                    break
            actions.move_to_element(next_button).perform()
            time.sleep(1)
            next_button.click()

            # 输入用户名, 有时候这个页面会没有
            try:
                user_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[data-testid="ocfEnterTextTextInput"]')))
                user_input.send_keys(x_username)
                # 点击下一步
                next_buttons_2 = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'button[role="button"]')))
                for i, button in enumerate(next_buttons_2):
                    print(f"username Button {i+1} HTML:")
                    print(button.text)
                    if button.text == "Next" or button.text == "下一步":
                        next_button = button
                        break
                actions.move_to_element(next_button).perform()
                time.sleep(10)
                next_button.click()
            except:
                logging.error("直接输入密码...",)

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
            # print("cookies:",cookies)
            self.save_cookies(cookies, uid)
            time.sleep(1)
            return True
        except:
            logging.error("login",traceback.format_exc())
            return False
    def x_login_new(self, response, user):
        try:
            x_email = user['email']
            x_password = user['password']
            x_username = user['username']
            uid = user['id']
            driver = response.request.meta["driver"]
            wait = WebDriverWait(driver, 60)  # 设置最大等待时间为10秒
            
            # 找到登录用户名input
            email_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[autocomplete="username"]')))
            email_input.send_keys(x_username)

            # 点击下一步
            actions = ActionChains(driver)
            next_buttons = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'button[role="button"]')))
            next_button = next_buttons[3]
            actions.move_to_element(next_button).perform()
            time.sleep(1)
            next_button.click()

             # 输入密码
            password_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[name="password"]')))
            password_input.send_keys(x_password)

            # 点击登录
            login_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-testid="LoginForm_Login_Button"]')))
            actions.move_to_element(login_button).perform()
            time.sleep(1)
            login_button.click()

            # 等待页面 URL 发生变化，表示登录完成
            wait.until(EC.url_changes(driver.current_url))
            time.sleep(3)
            # 获取当前页面的所有 cookie
            cookies = driver.get_cookies()
            # print("cookies:",cookies)
            self.save_cookies(cookies, uid)
            time.sleep(10)
            return True

        except:
            logging.error("login",traceback.format_exc())
            return False
    def save_cookies(self, cookies, uid:int):
        # cookies = [{'domain': '.x.com', 'expiry': 1766215508, 'httpOnly': False, 'name': 'twid', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'u%3D1869988014640046080'}, {'domain': 'x.com', 'httpOnly': False, 'name': 'lang', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'en'}, {'domain': '.x.com', 'expiry': 1769239506, 'httpOnly': False, 'name': 'ct0', 'path': '/', 'sameSite': 'Lax', 'secure': True, 'value': '365a776e07757a3e38e8c15f037f9b9619f736f37f07fa48707e1e5492fa7c995d60866402b910e13c06c62ed3f55363f8c924050f455b538467705592872668598c9eb300e1931630c9063213278eda'}, {'domain': '.x.com', 'expiry': 1734765906, 'httpOnly': True, 'name': 'att', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': '1-MEsfpCtuxcJC8zV2cD2OS1P1H3WlD4aRGhX5w6ZE'}, {'domain': '.x.com', 'expiry': 1769239506, 'httpOnly': True, 'name': 'auth_token', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': '798ca81c9d2d09a098da7e4308acf968969fcf82'}, {'domain': '.x.com', 'expiry': 1766215508, 'httpOnly': False, 'name': 'personalization_id', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': '"v1_KBPOnz9E4KcPMsN2eyHIAQ=="'}, {'domain': '.x.com', 'expiry': 1769239506, 'httpOnly': True, 'name': 'kdt', 'path': '/', 'sameSite': 'Lax', 'secure': True, 'value': 'oxPJksv12hD9n5btUXuvNBA6DkpN7dtzxFV6nucu'}, {'domain': '.x.com', 'expiry': 1766215507, 'httpOnly': False, 'name': 'night_mode', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': '2'}, {'domain': '.x.com', 'expiry': 1769239508, 'httpOnly': False, 'name': 'guest_id_ads', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'v1%3A173467952393767084'}, {'domain': '.x.com', 'expiry': 1734688493, 'httpOnly': False, 'name': 'gt', 'path': '/', 'sameSite': 'Lax', 'secure': True, 'value': '1870007578304094359'}, {'domain': '.x.com', 'expiry': 1769239508, 'httpOnly': False, 'name': 'guest_id_marketing', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'v1%3A173467952393767084'}, {'domain': '.x.com', 'expiry': 1766215493, 'httpOnly': False, 'name': 'guest_id', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': '173467952393767084'}]
        cookie_file = get_cookies_file(uid)
        os.makedirs(os.path.dirname(cookie_file), exist_ok=True)
        with open(cookie_file, 'w+') as file:  # 以文本模式打开文件
            json.dump(cookies, file, indent=4) 
    


