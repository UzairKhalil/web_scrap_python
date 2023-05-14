from bs4 import BeautifulSoup
from selenium import webdriver
import os
from joblib import Parallel, delayed

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
service = webdriver.chrome.service.Service(executable_path=os.getcwd() + "./chromedriver.exe")
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.set_page_load_timeout(900)

base_link = 'https://www.catch.com.au/seller/vdoo/products.html?page='
page_number = 1
product_links = []

while page_number != 2:
    link = base_link + str(page_number)
    driver.get(link)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    links = soup.find_all("a", class_="css-1k3ukvl")

    if not links:
        break
    
    hrefs = []
    for link in links:
        href = link.get("href")
        if href.startswith("/"):
            href = "https://www.catch.com.au" + href
        hrefs.append(href)

    product_links += hrefs
    page_number += 1

driver.quit()

def scrape_product_page(href):
    driver = webdriver.Chrome(service=service, options=chrome_options)
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
    driver.quit()
    return product

products = Parallel(n_jobs=-1, verbose=1)(
    delayed(scrape_product_page)(href) for href in product_links)

print(len(hrefs))
print(len(products))
