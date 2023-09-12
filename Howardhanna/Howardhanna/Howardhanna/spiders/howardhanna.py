# -*- coding: utf-8 -*-
import scrapy


class HowardhannaSpider(scrapy.Spider):
    name = 'howardhanna'
    allowed_domains = ['howardhanna.com']
    start_urls = ['http://howardhanna.com/']

    def parse(self, response):
        
        
        pass
