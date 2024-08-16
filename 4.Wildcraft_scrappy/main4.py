from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException

# Setup Firefox options
options = Options()
options.headless = True  # Run in headless mode (no GUI)

# Initialize WebDriver with Firefox
driver = webdriver.Firefox(service=Service(), options=options)
content = []
page = 1
while True:
    # Load the webpage
    driver.get(f'https://wildcraft.com/women/clothing/jackets-cheaters?page={page}')

    # Wait for the content to load if necessary
    driver.implicitly_wait(40)

    # Extract product names (example selector)
    products = driver.find_elements(By.CSS_SELECTOR, "div.item-productItem-Pnf")

    driver.implicitly_wait(10)

    if len(products) == 0:
        break

    for product in products:
        try:
            # Extract product name
            name = product.find_element(By.CSS_SELECTOR, "span[itemprop='name']").text
            
            try:
            # Extract product price
                price_element = product.find_element(By.CSS_SELECTOR, "div.priceRange-specialPrice-PjY")
                price = price_element.text

            except NoSuchElementException:

                price = None
            
            try:
            # Extract discount % 
                discount_element = product.find_element(By.CSS_SELECTOR, "div.priceRange-saleBadge-Var")
                discount = discount_element.text

            except NoSuchElementException:

                discount = None



            print(f"Product Name: {name}, Price: {price}, Discount: {discount}")

        except NoSuchElementException as e:
            
            print(f"Error extracting product data: {e}")

    page += 1

# Close the browser
driver.quit()
