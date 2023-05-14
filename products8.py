import requests
from bs4 import BeautifulSoup

api_url = "https://www.catch.com.au/seller/vdoo/products.json"

max_pages = 2  # <-- set the maximum number of pages to scrape

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
        price = soup.select_one('[itemprop=price]')
        title = soup.h1.text.strip() if soup.h1 else None
        if price:
            product = {"title": title, "price": price.get('content')}
            product_list.append(product)
        else:
            print(f"Price not found for {title}")
    if not results or params['page'] >= max_pages:
        break
    params["page"] += 1

print(f"Scraped {len(product_list)} products in total")
print(product_list)
