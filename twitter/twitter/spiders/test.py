import scrapy
from scrapy_selenium import SeleniumRequest
from twitter.gptapi import GPTAPI


class TestSpider(scrapy.Spider):
    name = "test"
    allowed_domains = ["x.com"]
    start_urls = ["https://x.com"]

    def start_requests(self):
        message = """
        有谁知道最近哪些meme币比较有前景啊？
        """
        res = GPTAPI().get_cn_response(message)
        print(res)
        return
        yield SeleniumRequest(url=self.start_urls[0], callback=self.parse)
    def parse(self, response):
        print("hello")
