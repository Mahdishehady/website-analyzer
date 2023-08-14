import requests
from bs4 import BeautifulSoup
import json


class WebScraper:
    def __init__(self, url):
        self.url = url

    def fetch_page_content(self):
        response = requests.get(self.url)
        return response.text

    def scrape_json_ld(self):
        page_content = self.fetch_page_content()
        soup = BeautifulSoup(page_content, "html.parser")

        json_ld_script = soup.find("script", {"type": "application/ld+json"})

        if json_ld_script:
            json_ld_content = json_ld_script.string

            try:
                json_ld_data = json.loads(json_ld_content)
                return json_ld_data
            except json.JSONDecodeError:
                print("Failed to parse JSON-LD data.")
        else:
            print("JSON-LD script tag not found on the page.")
            return None


url = "https://www.almayadeen.net"
scraper = WebScraper(url)

json_ld_data = scraper.scrape_json_ld()

if json_ld_data:
    print("JSON-LD Data:")
    print(json_ld_data)
    print("Number of items:", len(json_ld_data))
