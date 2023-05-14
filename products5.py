import requests
from bs4 import BeautifulSoup

api_url = "https://www.catch.com.au/seller/vdoo/products.json"

params = {
    "page": 1,  # <-- to get other pages, increase this parameter
}

data = requests.get(api_url, params=params).json()

urls = []
products = []
for r in data['payload']['results']:
    urls.append(f"https://www.catch.com.au{r['product']['productPath']}")
    print(len(urls))

for url in urls:
    soup = BeautifulSoup(requests.get(url).content, 'html.parser')
    price = soup.select_one('[itemprop=price]')['content']
    title = soup.h1.text
    product = {"title": title,"price": price}
    products.append(product)
    print(f'{title:<100} {price:<5}')
    # print(len(product))
    # print(product)