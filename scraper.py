import requests
from bs4 import BeautifulSoup
import json

class Scraper:
    def __init__(self, max_pages):
        # Intialized max pages to be extracted and source URL
        self.max_pages = max_pages
        self.base_url = "https://dentalstall.com/shop/?page={}"

    def scrape(self):
        all_products = []

        for page_num in range(1, self.max_pages + 1):
            url = self.base_url.format(page_num)
            print(f"Scraping page {page_num}...")

            try:
                # Fetches all the data from URL
                response = requests.get(url)
                # Handles error scenario
                response.raise_for_status()

                page_content = response.content
                self.parse_page(page_content, all_products)

            except requests.exceptions.RequestException as e:
                print(f"Error fetching page {page_num}: {e}")
                continue

        print(f"Scraping complete. {len(all_products)} products scraped.")
        
        self.save_to_file(all_products)
        
        return all_products

    def parse_page(self, page_content, all_products):
        # Extract Data
        soup = BeautifulSoup(page_content, "html.parser")

        product_elements = soup.select("#mf-shop-content > ul > li")

        for product_element in product_elements:
            # get product title
            title_element = product_element.select_one("div > div.mf-product-details > div.mf-product-content > h2")
            product_title = title_element.text.strip() if title_element else None

            # Get price
            price_element = product_element.select_one("div > div.mf-product-details > div.mf-product-price-box > span.price")
            product_price = price_element.text.strip() if price_element else None

            # Get the image URL
            image_element = product_element.select_one("div.mf-product-thumbnail img")
            image_url = image_element['src'] if image_element else None

            # push the data to save - if all three fields are found
            if product_title and product_price and image_url:
                product = {
                    "product_title": product_title,
                    "product_price": product_price,
                    "path_to_image": image_url
                }
                all_products.append(product)

        print(f"Found {len(all_products)} products on this page.")
    
    def save_to_file(self, data):
        # Save the data to a JSON file
        with open("scraped_data.json", "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        print("Scraped data saved to scraped_data.json.")

# As of now max_pages set as 5 , can be adjustable
scraper = Scraper(max_pages = 5)
scraped_data = scraper.scrape()
print(json.dumps(scraped_data, indent=4))
