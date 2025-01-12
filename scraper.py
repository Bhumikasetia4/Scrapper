from fastapi import FastAPI
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup
import json

app = FastAPI()

class Product(BaseModel):
    product_title: str
    product_price: str
    path_to_image: str

class Scraper:
    def __init__(self, max_pages):
        self.max_pages = max_pages
        self.base_url = "https://dentalstall.com/shop/?page={}"

    def scrape(self):
        all_products = []
        for page_num in range(1, self.max_pages + 1):
            url = self.base_url.format(page_num)
            try:
                response = requests.get(url)
                response.raise_for_status()
                page_content = response.content
                self.parse_page(page_content, all_products)
            except requests.exceptions.RequestException as e:
                continue
        return all_products

    def parse_page(self, page_content, all_products):
        soup = BeautifulSoup(page_content, "html.parser")
        product_elements = soup.select("#mf-shop-content > ul > li")

        for product_element in product_elements:
            title_element = product_element.select_one("div > div.mf-product-details > div.mf-product-content > h2")
            product_title = title_element.text.strip() if title_element else None
            price_element = product_element.select_one("div > div.mf-product-details > div.mf-product-price-box > span.price")
            product_price = price_element.text.strip() if price_element else None
            image_element = product_element.select_one("div.mf-product-thumbnail img")
            image_url = image_element['src'] if image_element else None
            if product_title and product_price and image_url:
                product = {
                    "product_title": product_title,
                    "product_price": product_price,
                    "path_to_image": image_url
                }
                all_products.append(product)

    def save_to_file(self, data):
        # Save the data to a JSON file
        with open("scraped_data.json", "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        print("Scraped data saved to scraped_data.json.")

@app.post("/scrape", response_model=list[Product])
def get_scraped_data():
    scraper = Scraper(max_pages=5)
    scraped_data = scraper.scrape()
    
    # Save the scraped data to a JSON file
    scraper.save_to_file(scraped_data)
    
    return scraped_data
