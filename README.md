# Scrapper

A simple web scraper to extract product details (title, price, and image) from a shopping website: Dentalstall. This scraper supports multiple pages, and the data is saved to a `scraped_data.json` file.

## Features
- Scrapes product title, price, and image URL.
- Handles errors when fetching pages.
- Extracts data from multiple pages (can be customized via `max_pages`).
- Saves the extracted data to a JSON file.

## Prerequisites
Before running the scraper, ensure that you have the following installed:

- Python 3.6 or higher
- `requests` library
- `beautifulsoup4` library

To install the required libraries, you can use pip:

```bash
pip install requests beautifulsoup4

Run the script to start scraping data:
python scraper.py


