import httpx
from selectolax.parser import HTMLParser
import json
import os
from urllib.parse import urlparse

#footwear #camping-and-hiking

def extract_text(html, sel):
        """
        Extracts the text from the given HTML based on the provided CSS selector.

        Args:
            html (HTMLParser): The HTML parser object.
            sel (str): The CSS selector to extract the text from.

        Returns:
            str: The extracted text, or None if the extraction fails.
        """
        try:
            return html.css_first(sel).text().lower()
        except AttributeError:
            return None 

def extract_attribute(html, sel, attr):
    """ Extracts the value of a specific attribute from the first element in the HTML
    that matches the given CSS selector.
    Args:
        html (HTMLParser): The HTML parser object.
        sel (str): The CSS selector to match the element.
        attr (str): The attribute to extract the value from.
    Returns:
        str: The value of the attribute, or None if the extraction fails.
        """
    try:
        return f"https://www.rei.com{html.css_first(sel).attributes.get(attr)}"
    except AttributeError:
        return None


def write_file(filename, content):
    """
    Writes the content to a file specified by the filename parameter.

    Args:
        filename (str): The name of the file to write the content to.
        content (list): A list of strings representing the content to be written.

    Returns:
        None
    """
    try:
        with open(filename, 'w') as file:
            json.dump(content, file, indent=4)
    except Exception as e:
        return e
def extract_subcategory(url):
    """
    Extracts the subcategory from a given REI URL.
    
    Args:
        url (str): The URL string from which to extract the subcategory.
    
    Returns:
        str: The extracted subcategory text.
    """
    try:
        path = urlparse(url).path  # Extract the path from the URL
        subcategory = path.split('/')[2]  # The subcategory is the third element in the path
        return subcategory
    except IndexError:
        return None

folder_list= ["cycling","fitness"] #, "womens-clothing", "mens-clothing", "cycling"

for folder in folder_list:
    path = f"C:\\Users\\ranje\\OneDrive\\D_Folder\\Webscrapping\\3.Multi_category_with_sub_categ\\{folder}"
    os.makedirs(path, exist_ok=True)
    #create list to store the href links of the sub categories 
    #sub_cat_links=[]

    furl = f"https://www.rei.com/c/{folder}/f/scd-deals"
    fheaders = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0"}
    fresp = httpx.get(furl, headers=fheaders)
    fhtml = HTMLParser(fresp.text)
    hrefs = fhtml.css("a.EmmdSBUU6nIcU_I7KcX5")

    sub_cat_list =[]
    hrefs_link=[]
    href_title =[]
    for href in hrefs:
        
        sub_cat_list.append(extract_text(href,"a.EmmdSBUU6nIcU_I7KcX5"))
        hrefs_link.append(extract_attribute(href,"a.EmmdSBUU6nIcU_I7KcX5", "href"))
        href_title.append(extract_subcategory(extract_attribute(href,"a.EmmdSBUU6nIcU_I7KcX5", "href")))


    print(href_title)
    print(len(href_title))

    for category in href_title:
        content = []
        page = 1
        while True:
            if page == 1:    
                url = f"https://www.rei.com/c/{category}/f/scd-deals"
            else:
                url = f"https://www.rei.com/c/{category}/f/scd-deals?page={page}"

            # headers are mimic the browser headers from the browser used to access the site 
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0"}
            # httpx is same as requests but with some extra features like http2 and proxies 
            resp = httpx.get(url, headers=headers)
            #html parser is used to parse the html from the response text 
            html = HTMLParser(resp.text)
                #print(html.css_first("title").text())
            #html.css is used to select the elements from the html based on the css selector
            products = html.css("li.VcGDfKKy_dvNbxUqm29K")

            #if the length of products is 0 then break the loop
            if len(products) == 0:
                break
            #for each product in products object extract the name, price and image
            for product in products:
                item={
                    "Name": extract_text(product,".Xpx0MUGhB7jSm5UvK2EY"),
                    "Price": extract_text(product,"span[data-ui=sale-price]"),
                    "Image": extract_attribute(product,"img", "src")
                }
                # json.dumps is used to convert the item dictionary to a string
                
                content.append(item)
            page += 1
        # write each category content to a json or txt file seperately
        #(.json or txt )
        write_file(f"C:\\Users\\ranje\\OneDrive\\D_Folder\\Webscrapping\\3.Multi_category_with_sub_categ\\{folder}\\{category}.json",content)
        # print the length of content and the name of the category when each category is processed
        print(f"{len(content)} items written to {category}.json")