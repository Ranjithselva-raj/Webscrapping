import httpx
from selectolax.parser import HTMLParser
import csv
import json


#footwear #camping-and-hiking

def extract_text(html, sel):
        try:
            return html.css_first(sel).text()
        except AttributeError:
            return None 

def extract_attribute(html, sel, attr):
    try:
        return html.css_first(sel).attributes.get(attr)
    except AttributeError:
        return None


def write_file(filename, content):
        with open(filename, 'w') as file:
            for line in content:
                file.write(line+'\n')


Category_list= ["cycling", "camping-and-hiking", "womens-clothing", "mens-clothing"] #, "womens-clothing", "mens-clothing", "cycling"

for category in Category_list:
    content=[]
    page = 1
    while True:
        if page == 1:    
            url = f"https://www.rei.com/c/{category}/f/scd-deals"
        else:
            url = f"https://www.rei.com/c/{category}/f/scd-deals?page={page}"
    
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0"}

        resp = httpx.get(url, headers=headers)
        html = HTMLParser(resp.text)
        #print(html.css_first("title").text())
        products = html.css("li.VcGDfKKy_dvNbxUqm29K")

        if len(products) == 0:
            break

        for product in products:
            item={
                "Name": extract_text(product,".Xpx0MUGhB7jSm5UvK2EY"),
                "Price": extract_text(product,"span[data-ui=sale-price]"),
                "Image": extract_attribute(product,"img", "src")
            }
            string_item = json.dumps(item)
            content.append(string_item)
        page += 1
    #write_file(category+".txt",content)
    write_file(category+".json",content)
    print(f"{len(content)} items written to {category}.json")