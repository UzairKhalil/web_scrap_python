import sys
import requests
from bs4 import BeautifulSoup
import csv
import datetime


url = "https://www.catch.com.au/seller/vdoo/products.html"
# url = input("Enter the URL of the products page: ")
if "/seller/" not in url or "/products.html" not in url:
    print("Invalid URL format")
    sys.exit(1)

api_url = url.replace("/products.html", "/products.json")
max_pages = 50
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
            quantity = quantity.find_all("option")[-1].text.strip()

        # Scraping Description
        description = soup.find("div", {"itemprop": "description"}).text.strip().replace('\n', '')

        # Scraping Images
        imagesrc_list = []
        image_tags = soup.select("img.css-110rls4")
        for index, image in enumerate(image_tags):
            imagesrc_list.append(f"img{index+1}: {image['src']}")


        # Scraping Other Sellers
        other_seller_list = []
        other_seller_tags = soup.select("div.css-cjxkrp li")
        for other_seller in other_seller_tags:
            seller_price = other_seller.find("meta", {"itemprop": "price"})["content"]
            other_seller_list.append({f"Seller{len(other_seller_list)+1}": "", f"Price{len(other_seller_list)+1}": seller_price})

        # Creating Product Dictionary
        product = {"Title": title, "Brand": brand, "Price": price, "Quantity": quantity}
        for i in range(len(imagesrc_list)):
            product[f"img{i+1}"] = imagesrc_list[i]
        product["Description"] = description
        for other_seller in other_seller_list:
            product.update(other_seller)
        
        product_list.append(product)

    if not results or params["page"] >= max_pages:
        break
    params["page"] += 1

print(f"Scraped {len(product_list)} products in total")
print(len(product_list))
# Exporting to CSV
csv_columns = []
for product in product_list:
    for key in product.keys():
        if key not in csv_columns:
            csv_columns.append(key)

# csv_file = "products.csv"
current_date = datetime.date.today().strftime("%d-%m-%Y")

csv_file = f"./csvs/products-{current_date}.csv"

try:
    with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for data in product_list:
            writer.writerow(data)
    print(f"Exported data to {csv_file}")
except IOError:
    print("I/O error")


