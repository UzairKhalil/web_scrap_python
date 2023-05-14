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

urls = []
products = []
for product_link in product_links:
    if product_link.has_attr("url"):  # add a condition to check if 'url' attribute exists
        url = product_link["url"]
        if url.startswith("/"):
            url = "https://www.catch.com.au" + url
        urls.append(url)

        driver.get(url)
        soup_prod = BeautifulSoup(driver.page_source, 'lxml')

        title = soup_prod.find("h1", class_="e12cshkt0").text.strip()
        price = soup_prod.find("span", class_="css-1qfcjyj").text.strip()
        image_link = soup_prod.find("img", class_="css-qvzl9f")["src"]
        product = {
            "title": title,
            "price": price,
            "image_link": image_link
        }
        products.append(product)
driver.quit()
print(len(products))
print(products)


# urls = []
# for product_link in product_links:
#     url = product_link.get("url")
#     if url.startswith("/"):
#         url = "https://www.catch.com.au" + url
#     urls.append(url)


# products = []
# for url in urls:
#     driver.get(url)
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