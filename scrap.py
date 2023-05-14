from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import os

# Set up Chrome WebDriver in headless mode
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument("--disable-gpu")
driver = webdriver.Chrome(os.getcwd() + "./chromedriver.exe", options=options)

# options = webdriver.ChromeOptions()
# options.add_argument("--headless")
# driver = webdriver.Chrome(options=options)

# Start on page 1
page_num = 1
last_href = None

# Loop through pages until we reach the last page
while True:
    # Construct link for current page
    link = f"https://www.catch.com.au/seller/vdoo/products.html?page={page_num}"
    driver.get(link)

    # Wait for page to load
    try:
        driver.implicitly_wait(10)
    except TimeoutException:
        # If the page takes too long to load, move on to the next page
        print(f"Timed out waiting for page {page_num}, moving on to the next page...")
        page_num += 1
        continue

    # Scrape page with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'lxml')
    auther_elements = soup.find_all("a", class_="css-1k3ukvl")

    # Extract href attributes
    hrefs = []
    for auther_element in auther_elements:
        href = auther_element.get("href")
        if href.startswith("/"):
            href = "https://www.catch.com.au" + href
        hrefs.append(href)

    # If there are no hrefs on this page, we've reached the last page
    if not hrefs:
        break

    # Save the last href on this page
    last_href = hrefs[-1]

    # Move to next page
    page_num += 1

# Print the last href from the last page
print(last_href)

# Clean up
driver.quit()
