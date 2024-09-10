from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Setup Firefox options
options = Options()
options.headless = True  # Run in headless mode (no GUI)

# Initialize WebDriver with Firefox
driver = webdriver.Firefox(service=Service(), options=options)

# Navigate to the website and load the initial page
driver.get('https://wildcraft.com/men/clothing/sweatshirts-pullovers?page=1')

seen_urls = []  # List to keep track of seen URLs

while True:
    try:
        # Get the current URL and check if it's been seen before
        current_url = driver.current_url
        if current_url in seen_urls:
            print("URL has been seen before. Ending extraction.")
            break
        else:
            seen_urls.append(current_url)

        # Click the "Show More" button to load more products
        try:
            show_more_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'navButton-root-sWY') and contains(@class, 'button-root_normalPriority-Z4b')]"))
            )
            show_more_button.click()
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.item-productItem-Pnf img[itemprop='image']"))
            )  # Adjust sleep time to ensure new products are loaded

        except (NoSuchElementException, TimeoutException, ElementClickInterceptedException):
            print("No more pages to load or unable to click 'Show More'.")
            break

    except Exception as e:
        print(f"Error during loop execution: {e}")
        break

# After all products have been loaded, extract product details
products = driver.find_elements(By.CSS_SELECTOR, "div.item-productItem-Pnf")
product_data = []
for product in products:
    try:
        # Extract product name
        name = product.find_element(By.CSS_SELECTOR, "span[itemprop='name']").text

        # Extract product price
        try:
            price_element = product.find_element(By.CSS_SELECTOR, "div.priceRange-specialPrice-PjY")
            price = price_element.text
        except NoSuchElementException:
            price = None

        # Extract discount %
        try:
            discount_element = product.find_element(By.CSS_SELECTOR, "div.priceRange-saleBadge-Var")
            discount = discount_element.text
        except NoSuchElementException:
            discount = None

        # Extract image URL
        #img_element = product.find_element(By.CSS_SELECTOR, "img[itemprop='image']")
        #img_url = img_element.get_attribute("src")

        # Append product details to the list
        product_data.append((name, price, discount))

    except NoSuchElementException as e:
        print(f"Error extracting product data: {e}")

# Print the final product data
for name, price, discount in product_data:
    print(f"Product Name: {name}, Price: {price}, Discount: {discount}")

# Close the browser
driver.quit()