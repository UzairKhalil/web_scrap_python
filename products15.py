import requests
from bs4 import BeautifulSoup

# Step 2: Send a request to the URL
# url = 'https://www.catch.com.au/product/plain-solid-colour-cushion-cover-covers-decorative-pillow-case-apple-green-22208832/?sid=VDOO&sp=1&st=24&srtrev=sj-spdvhyr2f9b5m2xd7jqe9k.click?pid=22208832&oid=74799711'
url = 'https://www.catch.com.au/product/2x-pure-natural-cotton-king-size-pillow-case-cover-slip-54x94cm-white-22208142/?sid=CASAMI&sp=2&st=7&srtrev=sj-wplmsyj0utfr5jrzach04t.click?pid=22208142&oid=74802607'
response = requests.get(url)
# Step 3: Parse the HTML
soup = BeautifulSoup(response.content, 'html.parser')
print(soup.prettify())
# # Step 5: Extract static data
# product_title = soup.select_one('h1.product-title').text.strip()
# product_price = soup.select_one('span.price').text.strip()
# product_description = soup.select_one('div.product-description').text.strip()
