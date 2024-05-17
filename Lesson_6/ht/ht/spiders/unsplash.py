from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from ..items import HtItem
import json


class UnsplashSpider(CrawlSpider):
    name = "unsplash"
    allowed_domains = ["unsplash.com"]
    start_urls = ["https://unsplash.com/"]
    rules = (Rule(LinkExtractor(restrict_xpaths=("//div[@class='h9Kv0']/ul/li/a")),  #callback='parse_category_urls',
                  follow=True),
             Rule(LinkExtractor(restrict_xpaths=('//div[@class="aD8H3"]/a')), callback='parse_photo_urls',
                  follow=False),)

    def parse_photo_urls(self, response):
        loader = ItemLoader(item=HtItem(), response=response)
        text = response.xpath('//script[@type="application/ld+json"]/text()').extract()
        meta_dict = json.loads(text[0])
        if meta_dict.get('isAccessibleForFree'):
            loader.add_value('name', meta_dict.get('name'))
            loader.add_value('image_urls', meta_dict.get('thumbnail').get('url'))  #.split('?')[0]+'.jpg')
            category = response.xpath('//span[@class="i_yon"]/a/text()').extract()
            loader.add_value('category', category)
        yield loader.load_item()
