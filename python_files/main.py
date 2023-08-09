import requests
from bs4 import BeautifulSoup
import push_to_mongodb
from post import Post

import datetime


def get_news(get_date):
    sitemap_url = f"https://www.aljazeera.net/sitemap.xml?yyyy={get_date.year}&mm={get_date.month}&dd={get_date.day}"
    response = requests.get(sitemap_url)
    sitemap_content = None
    if response.status_code == 200:
        sitemap_content = response.text
    else:
        print(f"Failed to fetch sitemap from {sitemap_url}")

    sitemap_soup = BeautifulSoup(sitemap_content, 'lxml')

    urls = [loc.text for loc in sitemap_soup.find_all('loc')]

    urls = [url for url in urls if
            not (url.endswith('.jpg') or url.endswith('.jpeg') or url.endswith('.png') or url.endswith('.gif'))]

    all_meta_data = []  # List to store all meta data from each page

    # for url in urls:
    # print(url)

    for url in urls:
        response = requests.get(url)
        print(url)
        if response.status_code == 200:
            page_content = response.text
            soup = BeautifulSoup(page_content, "lxml")

            # Find all meta tags on the page
            meta_tags = soup.find_all('meta')
            meta_data = {}
            # Extract meta data from each tag

            for tag in meta_tags:
                meta_data[tag.get('name')] = tag.get('content')
            meta_data = Post(meta_data).to_dict()
            print(meta_data)
            # elif tag.get('property'):
            #     meta_data[tag.get('property')] = tag.get('content')

            all_meta_data.append(meta_data)
    # push_data takes data and insert it to mongoDB
    push_to_mongodb.push_data(all_meta_data)

    # push_to_mongodb.select_data()
    # Write the meta data to a JSON file

    # with open("meta_data.json", "w", encoding="utf-8") as json_file:
    # json.dump(all_meta_data, json_file, ensure_ascii=False, indent=4)

    print("Meta data written to meta_data.json file.")


def get_news_by_dates(get_start_date, get_end_date):
    while not get_start_date == get_end_date:
        get_news(get_start_date)
        get_start_date = get_start_date + datetime.timedelta(days=1)


current_datetime = datetime.datetime.now()

last_10_days = current_datetime - datetime.timedelta(days=10)

get_news_by_dates(last_10_days, current_datetime)
