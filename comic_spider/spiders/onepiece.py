# -*- coding: utf-8 -*-
import scrapy

from ..items import ComicSpiderItem


class OnepieceSpider(scrapy.Spider):
    name = "onepiece"
    allowed_domains = ["onepiece.cc"]
    start_urls = ['http://onepiece.cc/']

    def parse(self, response):
        newest_sheet = response.xpath('//*[@id="main-area"]/article/div/div/div/div[2]/ul/li[1]')[0]
        chapter = ComicSpiderItem()
        chapter['published_date'] = newest_sheet.xpath('a/div[@class="baseinfo"]/p/text()').extract_first()
        chapter['title'] =  newest_sheet.xpath('a/p/text()').extract_first()
        chapter['url'] = self.start_urls[0] + newest_sheet.xpath('a/@href').extract_first()
        return chapter
