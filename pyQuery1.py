import os
from pyquery import PyQuery as pq
from scrapy import Selector
from selenium import webdriver

options = webdriver.FirefoxOptions()
options.add_argument('-headless')
# service = webdriver.FirefoxService(executable_path=os.getcwd() + './geckodriver.exe')
service = webdriver.Firefox(executable_path='./geckodriver.exe')
driver = webdriver.Firefox(service=service, options=options)

link = 'https://www.catch.com.au/seller/vdoo/products.html?page=1'
driver.get(link)

html = driver.page_source

# Using PyQuery to parse the HTML content
doc = pq(html)
auther_elements = doc('a.css-1k3ukvl')

# Extracting href attributes from the elements
hrefs = [a.attr('href') for a in auther_elements]

# Updating href values for internal links
hrefs = ['https://www.catch.com.au' + href if href.startswith('/') else href for href in hrefs]

print(len(hrefs))
print(hrefs)

driver.quit()
