import scrapy
import re
from ..items import HabrItem


class HabrSpider(scrapy.Spider):
    name = "habr"
    allowed_domains = ["career.habr.com"]
    start_urls = ["https://career.habr.com/vacancies?type=all"]

    def parse(self, response):
        item = HabrItem()
        for card in response.xpath("//*[@class='vacancy-card__inner']"):
            company = card.xpath(".//div[@class='vacancy-card__company-title']/a/text()").extract()
            item['company'] = company
            title = card.xpath(".//div[@class='vacancy-card__title']/a/text()").extract()
            item['title'] = title
            date = card.xpath(".//div[@class='vacancy-card__date']//time/text()").extract()
            item['date'] = date
            skill = card.xpath("//div[@class='vacancy-card__skills']")[7].extract()
            skill = re.sub(r'\<[^>]*\>', '',skill)
            item['skill'] = skill
            city = card.xpath("//div[@class='vacancy-card__meta']")[8].extract()
            city = re.sub(r'\<[^>]*\>', '', city)
            item['city'] = city

            yield item


