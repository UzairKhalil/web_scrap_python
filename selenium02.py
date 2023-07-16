import sys
import requests
from bs4 import BeautifulSoup
import csv
import datetime
url = "https://www.catch.com.au/seller/vdoo/products.html"
if "/seller/" not in url or "/products.html" not in url:
    print("Invalid URL format")
    sys.exit(1)
api_url = url.replace("/products.html", "/products.json")
max_pages = 1
params = {"page": 1}
product_list = []

while True:
    data = requests.get(api_url, params=params).json()
    results = data.get("payload", {}).get("results", [])
    print(f"Scraping page {params['page']}, {len(results)} products found")

    for r in results:
        product_url = f"https://www.catch.com.au{r['product']['productPath']}"
        response = requests.get(product_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        print(soup.prettify())
        break

    if not results or params["page"] >= max_pages:
        break
    params["page"] += 1

print(f"Scraped {len(product_list)} products in total")
print(product_list)
