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
        quantity = soup.find("select", {"id": "quantity-selector"})
        if quantity:
            quantity = quantity.find_all("option")[-1]["value"]

        # Scraping Image Src
        image_tags = soup.select("img.css-110rls4")
        imagesrc_list = []
        for index, image in enumerate(image_tags):
            imagesrc_list.append(f"img{index+1}: {image['src']}")

        # Scraping Description
        description = soup.find("div", {"itemprop": "description"}).text.strip()

        # Scraping Other Seller
        other_seller_list = []
        other_seller_tags = soup.select("li.css-1gy3o75.e5u7u070")
        for other_seller in other_seller_tags:
            seller_name = other_seller.find("span", {"class": "css-m1iedv"}).text.strip()
            seller_price = other_seller.find("meta", {"itemprop": "price"})["content"]
            other_seller_list.append({"Seller": seller_name, "Price": seller_price})

        product = {"Title": title, "Brand": brand, "Price": price, "Quantity": quantity, "ImageSrc": imagesrc_list, "Description": description, "OtherSeller": other_seller_list}
        product_list.append(product)

    if not results or params["page"] >= max_pages:
        break
    params["page"] += 1

print(f"Scraped {len(product_list)} products in total")
print(product_list)
