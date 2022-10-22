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
        "https://dantri.com.vn/giao-duc-huong-nghiep/khuyen-hoc",
        "https://dantri.com.vn/giao-duc-huong-nghiep/giao-duc-nghe-nghiep"
    ]

    urls = []
    for root_url in root_urls:
        urls.append(root_url)
        for page in range(1, pages, 1):
            urls.append(root_url + f"/trang-{page}.htm")

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

            time = "";

            getUrl = article.xpath('div/h3[@class="article-title"]/a/@href').get();

            if getUrl == None:
                continue

            urlCrawl = "https://dantri.com.vn" + getUrl

            page = requests.get(urlCrawl)

            soup = BeautifulSoup(page.content, "html.parser")

            job_elementsTime = soup.find("time", {"class": "author-time"})

            job_elementsContent = soup.find_all("div", {"class": "singular-content"})

            if job_elementsTime.has_attr("datetime"):
                time = job_elementsTime.attrs["datetime"]

            yield {
                'time': time,
                'url': urlCrawl,
                'category': response.xpath('//main/ol/li/h1/a/text()')[0].get(),
                'title': article.xpath('div/h3[@class="article-title"]/a/text()').get(),
                'summary': article.xpath('div/div[@class="article-excerpt"]/a/text()').get(),
                'content': ''.join([td.get_text() for content in job_elementsContent for td in content.find_all("p")])
            }


