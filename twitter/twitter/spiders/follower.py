import scrapy
from scrapy_selenium import SeleniumRequest
from selenium.webdriver import ActionChains
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 获取用户粉丝爬虫，只能获取最新的50条数据
class FollowerSpider(scrapy.Spider):
    name = "follower"
    allowed_domains = ["x.com","sannysoft.com"]
    start_urls = ["https://x.com/runtoweb3/verified_followers",
                  "https://x.com/runtoweb3/following",
                  "https://x.com/runtoweb3/followers"
                ]

    def start_requests(self):
        url = "https://x.com"
        self.cookies = [
           {'key': '_ga', 'value': 'GA1.2.517501193.1715931404'},
            {'key': '_monitor_extras', 'value': '{"deviceId":"t_Fn22UazWORcViKJcNm52","eventId":64,"sequenceNumber":64}'},
            {'key': 'amp_56bf9d', 'value': '719dce26-3184-486b-99e4-c70d7fca60c5...1ibr4819q.1ibr4as4l.12.kf.lh'},
            {'key': 'amp_669cbf', 'value': '719dce26-3184-486b-99e4-c70d7fca60c5.NzE5ZGNlMjYtMzE4NC00ODZiLTk5ZTQtYzcwZDdmY2E2MGM1..1i6oe4qnc.1i6oe7g55.1t.8.25'},
            {'key': 'att', 'value': '1-yGBxZNyuHc7FFT7cxkzu2cKGicRXhOFshIUUklPf'},
            {'key': 'auth_token', 'value': '467878901dd16a41310efb1faf317e16c4bd3f83'},
            {'key': 'ct0', 'value': '8530bba56b4014cc4ebdc059dca4ab768b11e6505209c246e3ab14ad722daef6449882562380d2b2be63be3a225f2f631c95cfdd72f03baf46c9ffe4a3cac580671e1259b487cab881b984191c17d376'},
            {'key': 'dnt', 'value': '1'},
            {'key': 'external_referer', 'value': 'padhuUp37zitFnzGTjTTopGUxwmEDamud2wJmFGZN3Q%3D|0|8e8t2xd8A2w%3D'},
            {'key': 'g_state', 'value': '{"i_l":0}'},
            {'key': 'kdt', 'value': '1ElRTjowgNW9UFPOZAuo1o2sjk4jU4PO7pe7WxPf'},
            {'key': 'lang', 'value': 'en'},
            {'key': 'guest_id', 'value': 'v1%3A173180809471346380'},
            {'key': 'personalization_id', 'value': "v1_oZrjEJ7rwHkKIbpDvM/GRg=="},
            {'key': 'twid', 'value': 'u%3D1854412414131068928'},
            {'key': 'first_ref', 'value': 'https%3A%2F%2Fwww.coingecko.com%2F'},
        ]
        yield SeleniumRequest(url=url, callback=self.parse)

    def parse1(self, response):
        driver = response.request.meta["driver"]
        # 给浏览器添加Cookie
        for item in self.cookies:
            driver.add_cookie({'name': item['key'], 'value': item['value']})
        time.sleep(5)
        driver.get(self.start_urls[2])
        wait = WebDriverWait(driver, 60)  # 设置最大等待时间为10秒
        elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[data-testid="cellInnerDiv"]')))
        # html_source = driver.page_source
        # print(html_source)
        # page_source = driver.page_source
        # aa = elements[0].get_attribute('outerHTML')
        
        for f in elements:
            aElements = f.find_element(By.CSS_SELECTOR, "a")
            url = aElements.get_attribute('href')
            name = url.split("/")[-1]
            with open('webpage.html', 'a', encoding='utf-8') as file:
                file.write(name + '\n')
       
    def parse(self, response):
        driver = response.request.meta["driver"]
        follows = []
        # 给浏览器添加Cookie
        for item in self.cookies:
            driver.add_cookie({'name': item['key'], 'value': item['value']})
        driver.get(self.start_urls[2])
        wait = WebDriverWait(driver, 60)  # 设置最大等待时间为10秒
        for x in range(0, 3):
            time.sleep(3)
            elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[data-testid="cellInnerDiv"]')))
            for f in elements:
                try:
                    aElements = f.find_element(By.CSS_SELECTOR, "a")
                    url = aElements.get_attribute('href')
                    name = url.split("/")[-1]
                    follows.append(name)
                except Exception as e:
                    break
            # 鼠标滚动，屏幕1920x1080,滚动三维之一屏
            ActionChains(driver) \
                .scroll_by_amount(0, 300) \
                .perform()
        unique_list = list(dict.fromkeys(follows))
        with open('webpagt.txt', 'a', encoding='utf-8') as file:
            file.write('\n'.join(unique_list))
       
    def parse_bot_test(self, response):
        driver = response.request.meta["driver"]
        driver.get('https://bot.sannysoft.com/')    #加载机器人检测页面，可以从各项指标判断当前程序是否为机器人
        source = driver.page_source
        with open('result.html', 'w') as f:
            f.write(source)
