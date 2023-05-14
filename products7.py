import requests
from bs4 import BeautifulSoup

api_url = "https://www.catch.com.au/seller/vdoo/products.json"

params = {
    "page": 1,
}

product_list = []

while True:
    data = requests.get(api_url, params=params).json()
    results = data.get('payload', {}).get('results', [])
    print(f"Scraping page {params['page']}, {len(results)} products found")
    for r in results:
        url = f"https://www.catch.com.au{r['product']['productPath']}"
        soup = BeautifulSoup(requests.get(url).content, 'html.parser')
        price = soup.select_one('[itemprop=price]')['content']
        title = soup.h1.text
        product = {"title": title, "price": price}
        product_list.append(product)
    if not results:
        break
    params["page"] += 1

print(f"Scraped {len(product_list)} products in total")
print(product_list)
