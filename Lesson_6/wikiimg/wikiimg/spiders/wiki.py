import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import WikiimgItem


class WikiSpider(CrawlSpider):
    name = "wiki"
    allowed_domains = ["commons.wikimedia.org"]
    start_urls = ["https://commons.wikimedia.org/wiki/Category:Featured_pictures_on_Wikimedia_Commons"]

    rules = (Rule(callback="parse_item", follow=True),)
    # LinkExtractor(allow=r"Items/"),
    def parse_item(self, response):
        for image in response.xpath('//*[@id="mw-category-media"]/ul/li/div/span/a/img'):
            file_url = image.xpath('@src').extract_first()
            print(file_url)
            item = WikiimgItem()
            item['file_urls'] = [file_url]
            item['original_file_name'] = file_url.split('/')[-1]
            yield item
