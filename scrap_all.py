from bs4 import BeautifulSoup
from selenium import webdriver
import os

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
service = webdriver.chrome.service.Service(executable_path=os.getcwd() + "./chromedriver.exe")
driver = webdriver.Chrome(service=service, options=chrome_options)

page_num = 1
hrefs = []

# while True:
while page_num != 3:
    link = f"https://www.catch.com.au/seller/vdoo/products.html?page={page_num}"
    driver.get(link)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    auther_elements = soup.find_all("a", class_="css-1k3ukvl")
    for auther_element in auther_elements:
        href = auther_element.get("href")
        if href.startswith("/"):
            href = "https://www.catch.com.au" + href
        hrefs.append(href)
    print(f"Processed page {page_num}, {len(hrefs)} links collected so far.")

    # check if there are no more products
    no_products_msg = soup.find("div", class_="css-wovpg2")
    if no_products_msg is not None:
        break

    page_num += 1

print(f"All pages processed, {len(hrefs)} links collected.")
print(hrefs)

driver.quit()
