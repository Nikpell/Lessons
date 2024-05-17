# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class HtItem(scrapy.Item):
    # define the fields for your item here like:
    category = scrapy.Field()
    photo_url = scrapy.Field()
    name = scrapy.Field()
    # img = scrapy.Field()
    image_urls = scrapy.Field()
    image_paths = scrapy.Field()
    images = scrapy.Field()

