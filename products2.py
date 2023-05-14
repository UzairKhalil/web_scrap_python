from bs4 import BeautifulSoup
from selenium import webdriver
import os

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
service = webdriver.chrome.service.Service(executable_path=os.getcwd() + "./chromedriver.exe")
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.set_page_load_timeout(900)

base_link = 'https://www.catch.com.au/seller/vdoo/products.html?page='
page_number = 1
products = []

while True:
    link = base_link + str(page_number)
    driver.get(link)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    product_links = soup.find_all("a", class_="css-1k3ukvl")

    if not product_links:
        break
    
    hrefs = []
    for product_link in product_links:
        href = product_link.get("href")
        if href.startswith("/"):
            href = "https://www.catch.com.au" + href
        hrefs.append(href)

    for href in hrefs:
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

    page_number += 1

driver.quit()
print(len(hrefs))
print(len(products))
