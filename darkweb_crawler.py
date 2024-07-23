import requests
from bs4 import BeautifulSoup
import time

class DarkWebCrawler:
    def __init__(self, base_url):
        self.base_url = base_url
        self.visited_links = set()
        self.proxies = {
            'http': 'socks5h://127.0.0.1:9050',
            'https': 'socks5h://127.0.0.1:9050'
        }

    def crawl(self, url):
        if url in self.visited_links:
            return
        self.visited_links.add(url)
        try:
            print(f"Attempting to access {url}")
            response = requests.get(url, proxies=self.proxies, timeout=30)
            if response.status_code == 200:
                print(f"Successfully accessed {url}")
                soup = BeautifulSoup(response.content, 'html.parser')
                self.process_page(soup)
                links = soup.find_all('a')
                for link in links:
                    href = link.get('href')
                    if href and href.startswith('http'):
                        self.crawl(href)
            else:
                print(f"Failed to access {url}: Status code {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error accessing {url}: {e}")
            time.sleep(5) 

    def process_page(self, soup):
        title = soup.title.string if soup.title else 'No title found'
        print(f"Title: {title}")
        
        headings = {}
        for i in range(1, 7):
            headings[f"h{i}"] = [h.get_text(strip=True) for h in soup.find_all(f"h{i}")]
        print("Headings:", headings)

        paragraphs = [p.get_text(strip=True) for p in soup.find_all('p')]
        print("Paragraphs:", paragraphs)

        links = [a['href'] for a in soup.find_all('a', href=True)]
        print("Links:", links)

        images = [img['src'] for img in soup.find_all('img', src=True)]
        print("Images:", images)


crawler = DarkWebCrawler('http://rxmyl3izgquew65nicavsk6loyyblztng6puq42firpvbe32sefvnbad.onion/')
crawler.crawl(crawler.base_url)
