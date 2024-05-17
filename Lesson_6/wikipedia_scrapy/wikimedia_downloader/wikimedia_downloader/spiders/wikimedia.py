import scrapy
from ..items import WikiimgItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class WikimediaSpider(CrawlSpider):
    name = "wikimedia"
    allowed_domains = ["commons.wikimedia.org"]
    start_urls = ["https://commons.wikimedia.org/wiki/Category:Featured_pictures_on_Wikimedia_Commons"]

    rules = (
        Rule(LinkExtractor(allow=r'Items/'),
             callback='parse_item', follow=True),
    )

    def parse(self, response):
        for image in response.xpath('//*[@id="mw-category-media"]/ul/li/div/span/a/img'):
            file_url = image.xpath('@src').extract_first()
            item = WikiimgItem()
            item['file_urls'] = [file_url]
            item['original_file_name'] = file_url.split('/')[-1]
            yield item


