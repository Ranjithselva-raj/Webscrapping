import httpx
from selectolax.parser import HTMLParser
import time
import pandas as pd

url = "https://www.rei.com/c/footwear/f/scd-deals"
#footwear #camping-and-hiking
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0"}

def extract_text(html, sel):
    try:
        return html.css_first(sel).text()
    except AttributeError:
        return None 
def extract_attribute(html, sel, attr):
    try:
        return f"https://www.rei.com{html.css_first(sel).attributes.get(attr)}"
    except AttributeError:
        return None

def extract_product(url, headers):
    try:
        resp = httpx.get(url, headers=headers)
        html = HTMLParser(resp.text)
        #print(html.css_first("title").text())
        products = html.css("li.VcGDfKKy_dvNbxUqm29K")
        return products
    except Exception as e:
        print(e)
        

if __name__ == "__main__":
    products = extract_product(url, headers)
    product_file= []
    for product in products:
        item={
            "Name": extract_text(product,".Xpx0MUGhB7jSm5UvK2EY"),
            "Price": extract_text(product,"span[data-ui=sale-price]"),
            "Image": extract_attribute(product,"img", "src")
        }
        product_file.append(item)
        print(item)
    df = pd.DataFrame(product_file)
    df.to_csv("product.csv", index=False)
    