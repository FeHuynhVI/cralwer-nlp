"""
vnexpress crawler.
"""
import scrapy
import requests
from bs4 import BeautifulSoup 

def get_urls(pages=30):
    """Get urls for vnexpress categories. Each category may span hundreds of pages.    
    """
    root_urls = [
        "https://vnexpress.net/giao-duc/du-hoc",
        "https://vnexpress.net/giao-duc/tuyen-sinh",
        "https://vnexpress.net/giao-duc/tin-tuc",
        "https://vnexpress.net/giao-duc/chan-dung",
        "https://vnexpress.net/giao-duc/giao-duc-40",
        "https://vnexpress.net/giao-duc/hoc-tieng-anh",
    ]

    urls = []
    for root_url in root_urls:
        urls.append(root_url)
        for page in range(1, pages, 1):
            urls.append(root_url + f"-p{page}")

    print(len(urls))
    return urls


class VnexpressSpider(scrapy.Spider):

    name = 'vnexpress'

    custom_settings = {
        'FEED_FORMAT': 'json',
        'FEED_URI': 'data/vnexpress.json',
        'FEED_EXPORT_ENCODING': 'utf-8',
        'FEED_EXPORT_INDENT': 4,
    }

    start_urls = get_urls(pages=30)

    def parse(self, response):
        category = response._url
        for article in response.xpath('//article'):

            time = "";

            getUrl = article.xpath('div/a/@href').get()
            
            if getUrl == None:
                continue

            page = requests.get(getUrl)

            soup = BeautifulSoup(page.content, "html.parser")

            job_elementsContent = soup.find_all("article")

            job_elementsTime = soup.find_all("span", {"class": "time-now"})

            job_elementsComment= soup.find_all("div", {"class": "content-comment"})

            listComment = [td.get_text() for content in job_elementsComment for td in content.find_all("p", class_="full_content")]

            if job_elementsTime != None and len(job_elementsTime) > 9:
                time = job_elementsTime[0].get_text()

            yield {
                'time': time,
                'url': getUrl,
                'category': category,
                'title': article.xpath('div/a/@title').get(),
                'summary': article.xpath('p/a/text()').get(),
                'content': ''.join([td.get_text() for content in job_elementsContent for td in content.find_all("p", class_="Normal")]),
                'comment': listComment
            }

