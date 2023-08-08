import requests
from bs4 import BeautifulSoup
from post import Post
import push_to_mongodb
import datetime


class NewsScraper:
    def __init__(self):
        pass

    def fetch_page_content(self, url):
        response = requests.get(url)
        return response.text

    def scrape_meta_data(self, url):
        page_content = self.fetch_page_content(url)
        soup = BeautifulSoup(page_content, "lxml")

        meta_tags = soup.find_all('meta')
        meta_data = {}

        for tag in meta_tags:
            meta_data[tag.get('name')] = tag.get('content')

        return meta_data

    def get_news(self, get_date):
        sitemap_url = f"https://www.aljazeera.net/sitemap.xml?yyyy={get_date.year}&mm={get_date.month}&dd={get_date.day}"
        response = requests.get(sitemap_url)

        if response.status_code == 200:
            sitemap_content = response.text
            sitemap_soup = BeautifulSoup(sitemap_content, 'lxml')

            urls = [loc.text for loc in sitemap_soup.find_all('loc')]

            urls = [url for url in urls if
                    not (url.endswith('.jpg') or url.endswith('.jpeg') or url.endswith('.png') or url.endswith('.gif'))]

            all_meta_data = []

            for url in urls:
                print(url)
                meta_data = self.scrape_meta_data(url)
                meta_data = Post(meta_data).to_dict()
                print(meta_data)
                all_meta_data.append(meta_data)

            push_to_mongodb.push_data(all_meta_data)
            print("Meta data written to MongoDB.")

        else:
            print(f"Failed to fetch sitemap from {sitemap_url}")

    def get_news_by_dates(self, get_start_date, get_end_date):
        while not get_start_date == get_end_date:
            self.get_news(get_start_date)
            get_start_date = get_start_date + datetime.timedelta(days=1)


news_scraper = NewsScraper()
start_date = datetime.date(2023, 7, 20)
end_date = datetime.date(2023, 7, 27)
news_scraper.get_news_by_dates(start_date, end_date)
