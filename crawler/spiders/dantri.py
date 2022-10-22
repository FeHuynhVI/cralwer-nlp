"""
vnexpress crawler.
"""
import scrapy
import requests
from bs4 import BeautifulSoup 

def get_urls(pages=30):
    """Get urls for dantri categories. Each category may span hundreds of pages.    
    """
    root_urls = [
        "https://dantri.com.vn/",
        "https://dantri.com.vn/giao-duc-huong-nghiep/khuyen-hoc.htm",
        "https://dantri.com.vn/giao-duc-huong-nghiep/giao-duc-nghe-nghiep.htm"
    ]

    urls = []
    for root_url in root_urls:
        urls.append(root_url)
        for page in range(1, pages, 1):
            urls.append(root_url + f"-p{page}")

    print(len(urls))
    return urls


class DantriSpider(scrapy.Spider):
    name = 'dantri'
    custom_settings = {
        'FEED_FORMAT': 'json',
        'FEED_URI': 'data/dantri.json',
        'FEED_EXPORT_ENCODING': 'utf-8',
        'FEED_EXPORT_INDENT': 4,
    }

    start_urls = get_urls(pages=30)

    def parse(self, response):
        category = response._url
        for article in response.xpath('//article'):

            urlCrawl = article.xpath('div/a/@href').get()

            page = requests.get(urlCrawl)

            soup = BeautifulSoup(page.content, "html.parser")

            job_elements = soup.find_all("article")

            yield {
                'category': category,
                'url': urlCrawl,
                'title': article.xpath('div/a/@title').get(),
                'text': article.xpath('p/a/text()').get(),
                'content': ''.join([td.get_text() for job_element in job_elements for td in job_element.find_all("p", class_="Normal")])
            }

