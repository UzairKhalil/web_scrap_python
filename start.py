from bs4 import BeautifulSoup
from selenium import webdriver
import os
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
service = webdriver.chrome.service.Service(executable_path=os.getcwd() + "./chromedriver.exe")
driver = webdriver.Chrome(service=service, options=chrome_options)
link = 'https://www.catch.com.au/seller/vdoo/products.html?page=1'
# link = input("Enter the link to scrape: ")
driver.get(link)
soup = BeautifulSoup(driver.page_source, 'lxml')
auther_elements = soup.find_all("a", class_="css-1k3ukvl")
hrefs = []
for auther_element in auther_elements:
    href = auther_element.get("href")
    if href.startswith("/"):
        href = "https://www.catch.com.au" + href
    hrefs.append(href)
print(len(hrefs))
print(hrefs)
driver.quit()