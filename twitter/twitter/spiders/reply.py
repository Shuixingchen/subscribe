import scrapy
from scrapy_selenium import SeleniumRequest
from selenium.webdriver import ActionChains
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pymysql
import json
import os

class ReplySpider(scrapy.Spider):
    name = "reply"
    allowed_domains = ["x.com"]
    start_urls = ["https://x.com"]

    def start_requests(self):
        url = "https://x.com"
        file_path = self.get_cookies_file(1)
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                cookies = json.load(file)
            self.cookies = [{'key':cookie['name'], 'value':cookie['value']} for cookie in cookies]
        
        yield SeleniumRequest(url=url, callback=self.do_post_reply)


    def do_post_reply(self, response):  
        reply_list = self.get_reply_list()
        for reply in reply_list:
            if reply['user_name'] == "":
                continue
            if reply['content'] == "":
                continue
            origin_post_url = self.post_replay(response,reply)
            if origin_post_url == "":
                continue
            reply['origin_post_url'] = origin_post_url
            self.save_reply_log(reply)
    def post_replay(self, response, reply):
        try:
            driver = response.request.meta["driver"]
            print("reply: ", reply)
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
            # print("article: ", article.get_attribute('outerHTML'))
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
            tweet_input.send_keys(reply['content'])
            # reply 按钮
            reply_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-testid="tweetButtonInline"]')))
            # 将鼠标移动到元素
            actions.move_to_element(reply_button).perform()
            time.sleep(1)
            reply_button.click()
            time.sleep(3)
            return last_url
        except Exception as e:
            print("Error: ", e)
            return ""

    def get_reply_list(self):
        try:
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
            query_big_user = """
            SELECT * from t_big_users
            """
            query_reply_content = """
            SELECT * from t_reply_content order by id desc limit 1
            """
            query_had_reply_today = """
            SELECT uid from t_reply_log where date(created_at)=curdate()
            """
            self.cursor.execute(query_big_user)
            users = self.cursor.fetchall()
            self.cursor.execute(query_reply_content)
            content = self.cursor.fetchone()
            self.cursor.execute(query_had_reply_today)
            had_reply_today = self.cursor.fetchall()
            reply_list = []
            for user in users:
                user_exists = any(user['id'] == row['uid'] for row in had_reply_today)
                if user_exists:
                    continue
                reply_list.append({
                    "user_id": user['id'],
                    "user_name": user['username'],
                    "content": content['content'],
                    "content_id": content['id']
                })
            return reply_list
        except Exception as e:
            print("Error: ", e)
    def save_reply_log(self, data):
        try:
            insert_log_sql = """
            INSERT INTO t_reply_log (uid, content_id,origin_post_url) VALUES (%s, %s,%s)
            """
            self.cursor.execute(insert_log_sql, (data['user_id'], data['content_id'], data['origin_post_url']))
            self.conn.commit()
        except Exception as e:
            print("Error: ", e)