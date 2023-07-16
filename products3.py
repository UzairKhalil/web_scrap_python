from bs4 import BeautifulSoup
from selenium import webdriver
import os

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
service = webdriver.chrome.service.Service(executable_path=os.getcwd() + "./chromedriver.exe")
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.set_page_load_timeout(900)


link = 'https://www.catch.com.au/seller/vdoo/products.html?page=1'
# link = 'https://www.catch.com.au/product/2x-pure-natural-cotton-king-size-pillow-case-cover-slip-54x94cm-white-22208142/'
# link = 'https://www.catch.com.au/product/2x-pure-natural-cotton-king-size-pillow-case-cover-slip-54x94cm-white-22208142/?sid=VDOO&sp=1&st=24&srtrev=sj-y6q8g76jidy47askjliuab.click?pid=22208142&oid=77988453'
driver.get(link)
soup = BeautifulSoup(driver.page_source, 'lxml')
# product_links = soup.find_all("div", class_="css-cjwokd")
# product_links = soup.find_all("select", class_="css-8httoy")
# title = soup.find("div", {"class": "css-cjwokd"})

# quantity = soup.find("e12cshkt0")s
title = soup.find_all("h1", class_="e12cshkt0").text.strip()

print(title)
# print (product_links)

# urls = []
# products = []
# for product_link in product_links:
#     if product_link.has_attr("url"):
#         url = product_link["url"]
#         if url.startswith("/"):
#             url = "https://www.catch.com.au" + url
#         urls.append(url)

#         driver.get(url)
#         soup_prod = BeautifulSoup(driver.page_source, 'lxml')

#         title = soup_prod.find("h1", class_="e12cshkt0").text.strip()
#         price = soup_prod.find("span", class_="css-1qfcjyj").text.strip()
#         image_link = soup_prod.find("img", class_="css-qvzl9f")["src"]
#         product = {
#             "title": title,
#             "price": price,
#             "image_link": image_link
#         }
#         products.append(product)
driver.quit()