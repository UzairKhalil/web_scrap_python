from bs4 import BeautifulSoup
import requests


url = 'https://www.amazon.com/Apple-MWP22AM-A-cr-AirPods-Renewed/dp/B0828BJGD2/?th=1'

response = requests.get(url)

# soup = BeautifulSoup(response.content, 'html.parser')

# title = soup.select('#productTitle')[0].get_text().strip()
# title = soup.find('span', id='productTitle')

# price = soup.select('#priceblock_ourprice')[0].get_text().strip()

html_content = response.content

soup = BeautifulSoup(html_content, 'html.parser')

print(soup.prettify())

