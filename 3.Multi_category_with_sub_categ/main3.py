import httpx
from selectolax.parser import HTMLParser
import json
import os
from urllib.parse import urlparse
import time

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
            text = html.css_first(sel).text().lower()
            print(f"extracted text: {text}")
            return text
        except AttributeError:
            print(f"failed to extracted text with sel: {sel}")
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
        attr_value = f"https://www.rei.com{html.css_first(sel).attributes.get(attr)}"
        print(f"extracted attribute: {attr_value}")
        return attr_value
    except AttributeError:
        print(f"failed to extracted attribute with sel: {sel}")
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
            print(f"File {filename} written successfully.")
    except Exception as e:
        print(f"Error writing file {filename}: {str(e)}")  # Print the error message
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
        print(f"extracted subcategory: {subcategory}")
        return subcategory
    except IndexError:
        print(f"failed to extracted subcategory with url: {url}")
        return None


def get_folder_open(folder,path_link):
    path = os.path.join(path_link,folder)
    os.makedirs(path, exist_ok=True)
    print(f"folder created: {path}")
    return path

def html_Parser_get_urllinks(folder):
    furl = f"https://www.rei.com/c/{folder}/f/scd-deals"
    fheaders = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0"}
    fresp = httpx.get(furl, headers=fheaders)
    fhtml = HTMLParser(fresp.text)
    hrefs = fhtml.css("a.EmmdSBUU6nIcU_I7KcX5")
    href_title =[]
    for href in hrefs:
        url= extract_attribute(href,"a.EmmdSBUU6nIcU_I7KcX5", "href")
        if url:
            subcategory = extract_subcategory(url)
            if subcategory:
                href_title.append(subcategory)
    print(f"length of href_title is {len(href_title)}")
    return href_title


   
def parse_url_links(href_title):
    all_content = []
    for category in href_title:
        content = []
        page = 1
        while True:
            if page == 1:    
                url = f"https://www.rei.com/c/{category}/f/scd-deals"
                print(f"fetching url: {url}")
            else:
                url = f"https://www.rei.com/c/{category}/f/scd-deals?page={page}"
                print(f"fetching url: {url}")
            try:
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
                    print(f"No products found, breaking.")
                    break
                #for each product in products object extract the name, price and image
                for product in products:
                    item={
                        "Name": extract_text(product,".Xpx0MUGhB7jSm5UvK2EY"),
                        "Price": extract_text(product,"span[data-ui=sale-price]"),
                        "Savings": extract_text(product,"div[data-ui=savings-percent-variant2]"),
                        "Image": extract_attribute(product,"img", "src")
                    }
                    content.append(item)
                page += 1
                time.sleep(1)
            except Exception as e:
                print(f"Error parsing url: {e}")
                break
        all_content.append((category,content))
    print(f"{len(all_content)}  sub categories  data appended to all_content")
    return all_content


def main():
    folder_list= ["cycling", "womens-clothing", "mens-clothing"] #, "womens-clothing", "mens-clothing", "cycling"
    path_link = "C:\\Users\\ranje\\OneDrive\\D_Folder\\Webscrapping\\3.Multi_category_with_sub_categ"
    for folder in folder_list:
        path = get_folder_open(folder,path_link)
        href_title = html_Parser_get_urllinks(folder)
        all_content = parse_url_links(href_title)
        for category, content in all_content:
            write_file(f"{path}\\{category}.json",content)
            print(f"{len(content)} items written to {category}.json")
    print("done")

if __name__ == "__main__":
    main()