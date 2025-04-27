import os
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
import time

def scrape_with_selenium(url, product_selector, title_selector, price_selector, output_folder="scraped_data", output_file="products.csv", driver_path=None):
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Setup Chrome options
    options = Options()
    options.add_argument("--headless")  # Headless mode
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    # Setup webdriver service
    if driver_path:
        service = ChromeService(executable_path=driver_path)
        driver = webdriver.Chrome(service=service, options=options)
    else:
        driver = webdriver.Chrome(options=options)  # Assumes chromedriver in PATH

    driver.get(url)
    time.sleep(3)  # wait for JS content to load

    products = driver.find_elements(By.CSS_SELECTOR, product_selector)
    print(f"Found {len(products)} products.")

    scraped_data = []

    for product in products:
        try:
            title = product.find_element(By.CSS_SELECTOR, title_selector).text.strip()
            price = product.find_element(By.CSS_SELECTOR, price_selector).text.strip()
            print(f"Product: {title} | Price: {price}")
            scraped_data.append({"title": title, "price": price})
        except Exception:
            continue

    driver.quit()

    # Save data to CSV
    csv_path = os.path.join(output_folder, output_file)
    with open(csv_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["title", "price"])
        writer.writeheader()
        writer.writerows(scraped_data)

    print(f"\nData saved to {csv_path}")

if __name__ == "__main__":
    # Example scraping Flipkart laptops search results
    flipkart_url = "https://www.flipkart.com/search?q=laptop"
    scrape_with_selenium(
        url=flipkart_url,
        product_selector="div._1AtVbE",
        title_selector="div._4rR01T, a.s1Q9rs",
        price_selector="div._30jeq3",
        output_folder="flipkart_output",
        output_file="laptops.csv"
        # driver_path="path_to_chromedriver"  # uncomment and set if needed
    )
