import scrapy
import json
import time
from scrapy_splash import SplashRequest
from crawler.items import ArticleItem,CatalogItem
from utils.date import convert_timestamp_to_localized_string
from utils.consts import BIANCE_DROP_CURRENCY_CATALOGID,BIANCE_ADD_CURRENCY_CATALOGID

class AnnouncementSpider(scrapy.Spider):
    name = 'announcement'
    allowed_domains = ['binance.com','www.binance.com','localhost']
    start_urls = ['https://www.binance.com/zh-CN/support/announcement/%E6%95%B0%E5%AD%97%E8%B4%A7%E5%B8%81%E5%8F%8A%E4%BA%A4%E6%98%93%E5%AF%B9%E4%B8%8A%E6%96%B0?c=48&navId=48&hl=zh-CN']
    # def start_requests(self):
    #     for url in self.start_urls:
    #         yield SplashRequest(url, self.parse, args={'wait': 0.5})
    def parse(self, response):
        script_content = response.css('script#__APP_DATA::text').get()
        print(script_content)
        scriptObj = json.loads(script_content)
        catalist = scriptObj['appState'].get('loader').get('dataByRouteId').get('d9b2').get('catalogs')
        for catalog in catalist:
            if catalog.get('catalogId') not in [BIANCE_ADD_CURRENCY_CATALOGID,BIANCE_DROP_CURRENCY_CATALOGID]:
                    continue
            catalogItem = CatalogItem()
            catalogItem['catalogId'] = catalog.get('catalogId')
            catalogItem['catalogName'] = catalog.get('catalogName')
            catalogItem['articles'] = []
            for article in catalog.get('articles'):
                articleItem = ArticleItem()
                articleItem['articleId'] = article.get('articleId')
                articleItem['title'] = article.get('title')
                releaseDate = article.get('releaseDate')/1000
                # 只保留10天内的公告
                if time.time()-releaseDate < 86400*10:
                    articleItem['releaseDate'] = convert_timestamp_to_localized_string(releaseDate)  
                    catalogItem['articles'].append(articleItem)
            print(catalogItem)
