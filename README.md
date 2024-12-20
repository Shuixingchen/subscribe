### 创建新爬虫项目
```shell
scrapy startproject crawler  # 会在当前目录创建一个biance目录，搭建了scrapy项目的脚手架
cd crawler
scrapy genspider announcement binance.com # 为项目创建爬取公告的爬虫
```

### 运行爬虫项目
```shell
cd crawler
scrapy crawl announcement
scrapy crawl follower
scrapy crawl xrequest

cd twitter
scrapy crawl post // 发送post

```