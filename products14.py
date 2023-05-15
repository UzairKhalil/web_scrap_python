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
        soup = BeautifulSoup(requests.get(product_url).content, "html.parser")
        title = soup.find("h1", {"class": "css-cit413 e12cshkt0"}).text.strip()
        brand = soup.find("a", {"itemprop": "brand"}).text.strip()
        price = soup.find("meta", {"itemprop": "price"})["content"]
        quantity = soup.find_all(class_="css-8httoy")
        if quantity:
            quantity = quantity.find_all("option")[-1].text.strip()
        description = soup.find("div", {"itemprop": "description"}).text.strip().replace('\n', '')
        imagesrc_list = []
        image_tags = soup.select("img.css-110rls4")
        for image in image_tags:
            imagesrc_list.append(image['src'])
        product = {"Title": title, "Brand": brand, "Price": price, "Quantity": quantity, "Product_URL": product_url}
        product["Description"] = description
        for i, src in enumerate(imagesrc_list):
            product[f"img{i+1}"] = src
        other_seller_list = []
        other_seller_tags = soup.select("div.css-cjxkrp li")
        for other_seller in other_seller_tags:
            seller_price = other_seller.find("meta", {"itemprop": "price"})["content"]
            other_seller_list.append({f"Seller{len(other_seller_list)+1}": "", f"Price{len(other_seller_list)+1}": seller_price})
        for other_seller in other_seller_list:
            product.update(other_seller)
        product_list.append(product)

    if not results or params["page"] >= max_pages:
        break
    params["page"] += 1

print(f"Scraped {len(product_list)} products in total")
print(product_list)

# csv_columns = []
# for product in product_list:
#     for key in product.keys():
#         if key not in csv_columns:
#             csv_columns.append(key)

# current_date = datetime.datetime.now().strftime("%d-%m-%Y_%H-%M")
# csv_file = f"{current_date}.csv"

# try:
#     with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
#         writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
#         writer.writeheader()
#         for data in product_list:
#             writer.writerow(data)
#     print(f"Exported data to {csv_file}")
# except IOError:
#     print("I/O error")
