from bs4 import BeautifulSoup
from selenium import webdriver
import os

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
service = webdriver.chrome.service.Service(executable_path=os.getcwd() + "./chromedriver.exe")
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.set_page_load_timeout(900)

link = 'https://www.catch.com.au/seller/vdoo/products.html?page=1'
driver.get(link)
soup = BeautifulSoup(driver.page_source, 'lxml')
product_links = soup.find_all("a", class_="css-1k3ukvl")

hrefs = []
for product_link in product_links:
    href = product_link.get("href")
    if href.startswith("/"):
        href = "https://www.catch.com.au" + href
    hrefs.append(href)

products = []

for href in hrefs[:3]:
    driver.get(href)
    soup = BeautifulSoup(driver.page_source, 'lxml')

    title = soup.find("h1", class_="e12cshkt0").text.strip()
    price = soup.find("span", class_="css-1qfcjyj").text.strip()
    image_link = soup.find("img", class_="css-qvzl9f")["src"]
    product = {
        "title": title,
        "price": price,
        "image_link": image_link
    }
    products.append(product)

driver.quit()
print(len(products))
print(products)
# # Split the list of hrefs into chunks of 5 and process them one by one
# for i in range(0, len(hrefs), 5):
#     hrefs_chunk = hrefs[i:i+5]
#     for href in hrefs_chunk:
#         try:
#             driver.get(href)
#             soup = BeautifulSoup(driver.page_source, 'lxml')
            
#             title = soup.find("h1", class_="e12cshkt0").text.strip()
#             price = soup.find("span", class_="css-1qfcjyj").text.strip()
#             image_link = soup.find("img", class_="css-qvzl9f")["src"]
#             product = {
#                 "title": title,
#                 "price": price,
#                 "image_link": image_link
#             }
#             products.append(product)
#         except Exception as e:
#             print(f"Error processing href {href}: {str(e)}")
    
# driver.quit()

# print(len(products))
# print(products)

# ===========================
# from bs4 import BeautifulSoup
# from selenium import webdriver
# import os
# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--headless")
# service = webdriver.chrome.service.Service(executable_path=os.getcwd() + "./chromedriver.exe")
# driver = webdriver.Chrome(service=service, options=chrome_options)
# driver.set_page_load_timeout(900)
# link = 'https://www.catch.com.au/seller/vdoo/products.html?page=1'
# driver.get(link)
# soup = BeautifulSoup(driver.page_source, 'lxml')
# product_links = soup.find_all("a", class_="css-1k3ukvl")

# hrefs = []
# for product_link in product_links:
#     href = product_link.get("href")
#     if href.startswith("/"):
#         href = "https://www.catch.com.au" + href
#     hrefs.append(href)
# products = []
# for href in hrefs:
#     driver.get(href)
#     soup = BeautifulSoup(driver.page_source, 'lxml')
    
#     title = soup.find("h1", class_="e12cshkt0").text.strip()
#     price = soup.find("span", class_="css-1qfcjyj").text.strip()
#     image_link = soup.find("img", class_="css-qvzl9f")["src"]
#     product = {
#         "title": title,
#         "price": price,
#         "image_link": image_link
#     }
#     products.append(product)
# driver.quit()
# print(len(products))
# print(products)
