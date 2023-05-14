# the following python web scraping program is working well and scraps the data from website. Now I want to grab more data from results like current i am getting price and title from it. here is the code:
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

# scrap the following these data from result 
# 1. Title: from <h1  class="css-cit413 e12cshkt0">.
# 2. Brand: from api_url like 'vdoo' in 'catch.com.au/seller/vdoo/'.
# 3. Price: which you are alreading scraping.
# 4. Quantity: from <select id="quantity-selector" class="css-8httoy"> check if quantity exists then get the last option value.
# 5. ImagesSrc: select the src of images from <img class="css-110rls4">. select all images and  store them in separately like img1, img2...
# 6. Decription: select all the Product Details inside it, <div itemprop="description" class="css-1oteowz">.
# 7. OtherSeller: now look for all the other sellers inside <li class='css-1gy3o75 e5u7u070'> and select Seller: from span.css-m1iedv and Price: from <meta itemprop="price" content="52.36" /> It should iterate and get all the other seller with thier prices.

# following is the html of this structure"
# <div class=css-1q971by>
# <div class=css-1s1jno5>
# <header class=css-sxfrcw>
# <h1 data-testid=product-title itemprop=name class="css-cit413 e12cshkt0">2x Pure Natural Cotton King Size Pillow Case Cover Slip - 54x94cm - White</h1>
# <div class=css-12dcq4d>
# <a href=/brand/casami text-decoration=underline itemprop=brand itemtype=https://schema.org/Brand itemscope class=css-rzn1xh>CASAMI<meta itemprop=name content=CASAMI></a>
# </div>
# </header>
# </div>
# <section class=css-198qm4s>
# <div class=css-c6j1qo>
# <div class=css-97gtxm>
# <div class="carousel css-1gzzu7g">
# <div class="verticalSlider___34ZFD carousel__slider carousel__slider--vertical" aria-live=polite tabindex=-1 role=listbox aria-label="Product gallery">
# <div class="carousel__slider-tray-wrapper verticalSlideTrayWrap___2nO7o carousel__slider-tray-wrap--vertical" style=height:0;padding-bottom:562.5%;width:100%>
# <div class="sliderTray___-vHFQ sliderAnimation___300FY carousel__slider-tray verticalTray___12Key carousel__slider-tray--vertical" style="display:flex;align-items:stretch;width:100%;transform:translateY(100%) translateY(0);flex-direction:column">
# <div tabindex=0 aria-selected=true role=option class="slide___3-Nqo carousel__slide carousel__slide--visible slide-height" style=width:unset;padding-bottom:unset;position:unset>
# <div class="slideInner___2mfX9 carousel__inner-slide" style=position:unset>
# <div tabindex=1 class=css-mebvip>
# <div class=css-1hpl62e>
# <div class=css-1paktoo>
# <img src=https://s.catch.com.au/images/product/0131/131541/6436350a33546263434513_w143h117.webp alt="2x Pure Natural Cotton King Size Pillow Case Cover Slip - 54x94cm - White" class=css-110rls4><link>
# </div>
# </div>
# </div>
# </div>
# </div>
# <div tabindex=0 aria-selected=true role=option class="slide___3-Nqo carousel__slide carousel__slide--visible slide-height" style=width:unset;padding-bottom:unset;position:unset>
# <div class="slideInner___2mfX9 carousel__inner-slide" style=position:unset>
# <div tabindex=2 class=css-mebvip>
# <div class=css-1hpl62e>
# <div class=css-1paktoo>
# <img src=https://s.catch.com.au/images/product/0131/131541/6436350adf90f052521259_w143h117.webp alt="2x Pure Natural Cotton King Size Pillow Case Cover Slip - 54x94cm - White" class=css-110rls4><link>
# </div>
# </div>
# </div>
# </div>
# </div>
# <div tabindex=0 aria-selected=true role=option class="slide___3-Nqo carousel__slide carousel__slide--visible slide-height" style=width:unset;padding-bottom:unset;position:unset>
# <div class="slideInner___2mfX9 carousel__inner-slide" style=position:unset>
# <div tabindex=3 class=css-mebvip>
# <div class=css-1hpl62e>
# <div class=css-1paktoo>
# <img src=https://s.catch.com.au/images/product/0131/131541/6436350b41ad7138238071_w143h117.webp alt="2x Pure Natural Cotton King Size Pillow Case Cover Slip - 54x94cm - White" class=css-110rls4><link>
# </div>
# </div>
# </div>
# </div>
# </div>
# </div>
# </div>
# </div>
# </div>
# </div>
# <div cursor=zoom-in class=css-6n1i8o>
# <img alt="2x Pure Natural Cotton King Size Pillow Case Cover Slip - 54x94cm - White" src=https://s.catch.com.au/images/product/0131/131541/6436350a33546263434513_w803h620.webp title="Preview image" class=css-qvzl9f>
# </div>
# </div>
# </section>
# <section class=css-eq6937>
# <div class=css-efv112>
# <div class=css-1rna3e>
# <div class=css-1qtcsfm>
# <div class=css-1msfinh>
# <div class="sell-price css-b9fkny" data-testid=product-price>
# <div class=css-8sgild>
# <div class=css-1b1lu52>
# <div data-testid=price-parts class=css-111drvy><span class=css-dpcpx8>$</span><span class="css-1qfcjyj ehnxcr60">46</span><span class=css-dpcpx8>99</span></div>
# </div>
# </div>
# </div>
# </div>
# </div>
# <div class=css-efv112>
# <div class=css-cjwokd><label for=quantity-selector class=css-q57j7z>Quantity</label></div>
# <div class=css-l1o170>
# <select aria-required=false aria-disabled=false width=100% color=typography.text id=quantity-selector class=css-8httoy>
# <option value=1>1</option>
# <option value=2>2</option>
# <option value=3>3</option>
# <option value=4>4</option>
# <option value=5>5</option>
# <option value=6>6</option>
# <option value=7>7</option>
# <option value=8>8</option>
# <option value=9>9</option>
# <option value=10>10</option>
# </select>
# <div class=css-1f91fwb>
# <span class=css-1dr9loy><svg viewBox="0 0 9 5" fill=currentcolor class=css-nkgpae>
# <title>select drop down arrow</title>
# <path d="M 0,0 V 2.1462796 L 4.3219228,5 8.5714286,2.1462796 V 0 L 4.3219228,2.5 Z"></path></svg></span>
# </div>
# </div>
# </div>
# <div class=css-1toz4si>
# <button aria-label="Add to wishlist" type=button class=css-l82ccg>
# <div class=css-1x0r6ti>
# <svg viewBox="0 0 24 24" fill=none fill-rule=evenodd clip-rule=evenodd stroke=currentColor stroke-width=2px class=css-1ha2345>
# <path d="M17.7008 4.33954C14.2668 3.01688 11.9914 6.06849 11.9914 6.06849C11.9914 6.06849 9.7347 3.00842 6.30068 4.33218C3.37802 5.45758 2.21316 8.81316 3.55237 11.5199C4.69898 13.8359 7.11958 16.8808 11.9914 20.2C16.8649 16.8808 19.3025 13.8432 20.4476 11.5273C21.7868 8.82015 20.6219 5.46494 17.7008 4.33954Z"></path>
# </svg>
# </div></button><button aria-label="Add to cart" class=css-o0n23k>Add to Cart</button><button aria-label="Buy now" class=css-evo4mt>Buy Now</button>
# </div>
# <div class=css-1vsr2v6>
# </div>
# </div>
# <div class=css-cjxkrp>
# <h5 class="css-10a25ll e12cshkt4">More buying options</h5>
# <ul itemtype=http://schema.org/AggregateOffer itemprop=offers itemscope class="css-1qtzlj5 e144sfsb0">
# <li itemtype=http://schema.org/Offer itemprop=offers itemscope class="css-2v4dzo e5u7u070">
# <div class=css-1arl00l>
# <div class=css-xe9tk1>
# </div>
# <div class=css-vvt8c5>
# <span class="css-d7paxp ehnxcr60">$46.99 </span><span itemtype=http://schema.org/Organization itemprop=seller itemscope class="css-l2rtr2 ehnxcr60">Free delivery. Sold by: <a href="/seller/grab-your-deals?oid=77988453&amp;soid=77988453" text-decoration=underline itemprop=name class=css-m1iedv>Grab Your Deals</a></span>
# </div>
# <a href="/product/2x-pure-natural-cotton-king-size-pillow-case-cover-slip-54x94cm-white-22208142/?sid=VDOO&amp;sp=1&amp;st=24&amp;srtrev=sj-25wrrjtj5l7pw96gzlfmje.click%3Fpid%3D22208142&amp;oid=77988453&amp;offer_id=77988453" itemprop=url class=css-1iunjvh>Select</a>
# </div>
# <meta itemprop=price content=46.99><meta itemprop=priceCurrency content=AUD><meta itemprop=availability content=http://schema.org/InStock>
# </li>
# <li itemtype=http://schema.org/Offer itemprop=offers itemscope class="css-1gy3o75 e5u7u070">
# <div class=css-1arl00l>
# <div class=css-xe9tk1></div>
# <div class=css-vvt8c5>
# <span class="css-d7paxp ehnxcr60">$52.36 </span><span itemtype=http://schema.org/Organization itemprop=seller itemscope class="css-l2rtr2 ehnxcr60">Free delivery. Sold by: <a href="/seller/vdoo?oid=74802607&amp;soid=77988453" text-decoration=underline itemprop=name class=css-m1iedv>VDOO</a></span>
# </div>
# <a href="/product/2x-pure-natural-cotton-king-size-pillow-case-cover-slip-54x94cm-white-22208142/?sid=VDOO&amp;sp=1&amp;st=24&amp;srtrev=sj-25wrrjtj5l7pw96gzlfmje.click%3Fpid%3D22208142&amp;oid=77988453&amp;offer_id=74802607" itemprop=url class=css-1iunjvh>Select</a>
# </div>
# <meta itemprop=price content=52.36><meta itemprop=priceCurrency content=AUD><meta itemprop=availability content=http://schema.org/InStock>
# </li>
# </ul>
# <meta itemprop=highPrice content=52.36><meta itemprop=lowPrice content=46.99><meta itemprop=offerCount content=2><meta itemprop=priceCurrency content=AUD>
# </div>
# </div>
# </section>
# <section class=css-2w60ma>
# <div class=css-12pfgnu>
# <div itemprop=description class=css-1oteowz>
# <p>
# <strong>Product Details:</strong><br>
# -This silk pillow case can protect and prolong the life of your pillow, so you and yours can always count on us to help deliver sweet dreams.
# </p>
# <p>
# <strong>Features:</strong><br>
# -100% fine natural cotton cover<br>
# -Anti-bacterial<br>
# -Breathable<br>
# -Hypoallergenic<br>
# -Envelope Closure<br>
# -Increases Pillow life<br>
# -Easy care machine washable
# </p>
# <p><strong>Specifications:</strong></p>
# <p>-Size: 54 x 94 cm</p>
# <p>
# <strong>Package Included:</strong><br>
# -2 x King Size Pillow Slip
# </p>
# <p>
# Notes:<br>
# -Actual colors may vary due to computer monitors displaying colors differently.<br>
# -Due to the nature of the manufacturing process and manual measurement, product sizing may vary slightly.
# </p>
# </div>
# </div>
# </section>
# </div>"
