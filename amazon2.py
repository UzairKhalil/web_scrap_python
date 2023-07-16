from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os

chrome_options = Options()
chrome_options.add_argument("--headless")
service = webdriver.chrome.service.Service(executable_path=os.getcwd() + "./chromedriver.exe")
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.set_page_load_timeout(900)

url = 'https://www.amazon.com/Apple-MWP22AM-A-cr-AirPods-Renewed/dp/B0828BJGD2/?th=1'

driver.get(url)

try:
    # Switch to iframe if necessary
    iframe = driver.find_element_by_id('desired-iframe-id')
    driver.switch_to.frame(iframe)

    # Locate the element using an alternative selector
    title_element = driver.find_element_by_css_selector('#productTitle')
    title = title_element.text.strip()

    print('Title:', title)
except:
    print('Element not found')

driver.quit()
