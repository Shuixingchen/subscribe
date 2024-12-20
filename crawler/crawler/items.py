# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
class ArticleItem(scrapy.Item):
    articleId = scrapy.Field()
    title = scrapy.Field()
    releaseDate = scrapy.Field()

class CatalogItem(scrapy.Item):
    catalogId = scrapy.Field()
    catalogName = scrapy.Field()
    articles = scrapy.Field()
