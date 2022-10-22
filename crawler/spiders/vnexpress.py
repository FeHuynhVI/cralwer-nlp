"""
vnexpress crawler.
"""
import scrapy
import framler     

def get_urls(pages=30):
    """Get urls for vnexpress categories. Each category may span hundreds of pages.    
    """
    root_urls = [
        "https://vnexpress.net/giao-duc",
        "https://vnexpress.net/giao-duc/chan-dung"
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
    ac = framler.AutoCrawlParser("requests")  

    def parse(self, response):
        category = response._url
        for article in response.xpath('//article'):
            urlCrawl = article.xpath('div/a/@href').get()
            yield {
                'category': category,
                'url': urlCrawl,
                'title': article.xpath('div/a/@title').get(),
                'text': article.xpath('p/a/text()').get(),
                'content': ac.parse(urlCrawl) 
            }

