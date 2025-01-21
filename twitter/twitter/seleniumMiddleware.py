
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from scrapy import signals

class SeleniumMiddleware:
    @classmethod
    def from_crawler(cls, crawler):
        # 这里可以访问到 crawler.settings 和 crawler.spider
        driver_arguments = crawler.settings.get('SELENIUM_DRIVER_ARGUMENTS')
        middleware = cls(
            driver_arguments=driver_arguments,
        )
        crawler.signals.connect(middleware.spider_closed, signal=signals.spider_closed)
        return middleware
    def __init__(self,driver_arguments):
        chrome_options = Options()
        for argument in driver_arguments:
            chrome_options.add_argument(argument)
        # 初始化 WebDriver
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

    def process_request(self, request, spider):
        """Process a request using the selenium driver if applicable"""
        self.driver.get(request.url)
        if hasattr(spider,'cookies'):
            for item in spider.cookies:
                self.driver.add_cookie({'name': item['key'], 'value': item['value']})
        if request.wait_until:
            WebDriverWait(self.driver, request.wait_time).until(
                request.wait_until
            )
        if request.screenshot:
            request.meta['screenshot'] = self.driver.get_screenshot_as_png()

        if request.script:
            self.driver.execute_script(request.script)

        body = str.encode(self.driver.page_source)

        # Expose the driver via the "meta" attribute
        request.meta.update({'driver': self.driver})

        return HtmlResponse(
            self.driver.current_url,
            body=body,
            encoding='utf-8',
            request=request
        )

    def spider_closed(self):
        self.driver.quit()