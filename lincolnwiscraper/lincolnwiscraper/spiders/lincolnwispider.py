import scrapy


class LincolnwispiderSpider(scrapy.Spider):
    name = "lincolnwispider"
    allowed_domains = ["co.lincoln.wi.us"]
    start_urls = ["https://co.lincoln.wi.us/meetings"]

    def parse(self, response):
        pass
