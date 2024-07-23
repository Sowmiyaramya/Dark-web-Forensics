import requests
from bs4 import BeautifulSoup
import scrapy

class DarkWebScraper(scrapy.Spider):
    name = "dark_web_scraper"
    start_urls = [
        "http://rxmyl3izgquew65nicavsk6loyyblztng6puq42firpvbe32sefvnbad.onion/"
    ]

    def parse(self, response):
        soup = BeautifulSoup(response.body, 'html.parser')
        for link in soup.find_all('a'):
            yield response.follow(link, self.parse)

        # Extract relevant data from the page
        title = soup.find('title').text
        text = soup.get_text()
        yield {
            'title': title,
            'text': text,
        }

if __name__ == "__main__":
    scrapy.crawl(DarkWebScraper)
