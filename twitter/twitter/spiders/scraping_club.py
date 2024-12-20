import scrapy
from scrapy_selenium import SeleniumRequest
from selenium.webdriver import ActionChains
import time
from selenium.webdriver.common.by import By

class ScrapingClubSpider(scrapy.Spider):
    name = "scraping_club"
    def start_requests(self):
        url = "https://scrapingclub.com/exercise/list_infinite_scroll/"
       
        yield SeleniumRequest(url=url, callback=self.parse)

    def parse(self, response):
        driver = response.request.meta["driver"]
        # scroll to the end of the page 10 times
        for x in range(0, 10):
            # scroll down by 10000 pixels
            ActionChains(driver) \
                .scroll_by_amount(0, 1000) \
                .perform()

            # waiting 2 seconds for the products to load
            time.sleep(2)

        # select all product elements and iterate over them
        for product in driver.find_elements(By.CSS_SELECTOR, ".post"):
            # scrape the desired data from each product
            url = product.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
            image = product.find_element(By.CSS_SELECTOR, ".card-img-top").get_attribute("src")
            name = product.find_element(By.CSS_SELECTOR, "h4 a").text
            price = product.find_element(By.CSS_SELECTOR, "h5").text

            # add the data to the list of scraped items
            yield {
                "url": url,
                "image": image,
                "name": name,
                "price": price
            }
