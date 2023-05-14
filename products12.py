import sys
import requests
from bs4 import BeautifulSoup
import csv

url = input("Enter the URL of the products page: ")
if "/seller/" not in url or "/products.html" not in url:
    print("Invalid URL format")
    sys.exit(1)

api_url = url.replace("/products.html", "/products.json")
max_pages = 2
params = {"page": 1}
product_list = []

while True:
    data = requests.get(api_url, params=params).json()
    results = data.get("payload", {}).get("results", [])
    print(f"Scraping page {params['page']}, {len(results)} products found")

    for r in results:
        product_url = f"https://www.catch.com.au{r['product']['productPath']}"
        soup = BeautifulSoup(requests.get(product_url).content, "html.parser")

        # Scraping Title
        title = soup.find("h1", {"class": "css-cit413 e12cshkt0"}).text.strip()

        # Scraping Brand
        brand = soup.find("a", {"itemprop": "brand"}).text.strip()

        # Scraping Price
        price = soup.find("meta", {"itemprop": "price"})["content"]

        # Scraping Quantity
        quantity_select = soup.find("select", {"id": "quantity-selector"})
        quantity = None
        if quantity_select:
            quantity = quantity_select.find_all("option")[-1]["value"]

        # Scraping Images
        imagesrc_list = []
        for index, image in enumerate(soup.select("img.css-110rls4")):
            imagesrc_list.append(image['src'])

        # Scraping Description
        description = soup.find("div", {"itemprop": "description"}).text.strip().replace('\n', '')

        # Scraping Other Sellers
        other_seller_list = []
        other_seller_tags = soup.select("ul.css-b1vjar-NavContainer li.css-1n0y31u")
        for other_seller in other_seller_tags[1:]:
            seller_name = other_seller.find("span", {"class": "css-m1iedv"}).text.strip()
            seller_price = other_seller.find("meta", {"itemprop": "price"})["content"]
            other_seller_list.extend([f"Seller{i+1}", seller_name, f"Price{i+1}", seller_price])

        product = {"Title": title, "Brand": brand, "Price": price, "Quantity": quantity, "Description": description}
        product.update({f"img{i+1}": imagesrc_list[i] for i in range(len(imagesrc_list))})
        product.update({other_seller_list[i]: other_seller_list[i+1] for i in range(0, len(other_seller_list), 2)})
        product_list.append(product)

    if not results or params["page"] >= max_pages:
        break
    params["page"] += 1

print(f"Scraped {len(product_list)} products in total")
print(product_list)
