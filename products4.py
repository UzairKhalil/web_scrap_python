import os
import scrapy
from scrapy.crawler import CrawlerProcess
from pyquery import PyQuery as pq
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Chrome


class CatchSpider(scrapy.Spider):
    name = "CatchSpider"
    start_urls = ['https://www.catch.com.au/seller/vdoo/products.html?page=1']

    def __init__(self):
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument("--headless")
        self.service = webdriver.chrome.service.Service(executable_path=os.getcwd() + "./chromedriver.exe")
        self.driver = webdriver.Chrome(service=self.service, options=self.chrome_options)

    def parse(self, response):
        html = response.text
        d = pq(html)
        auther_elements = d('a.css-1k3ukvl')
        hrefs = []
        for auther_element in auther_elements.items():
            href = auther_element.attr('href')
            if href.startswith("/"):
                href = "https://www.catch.com.au" + href
            hrefs.append(href)
        print(len(hrefs))
        print(hrefs)
        self.driver.quit()

if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(CatchSpider)
    process.start()
