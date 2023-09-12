from enum import unique
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re
import pandas as pd
from scrapy.cmdline import execute
import os
class DataCollectorBotSpider(CrawlSpider):
    name = 'data_collector_bot'
    allowed_domains = ['www.remax.com']
    # start_urls = ['https://www.remax.com/real-estate-agents?page=1&count=100']
    def start_requests(self):
        # os.remove('D:\\Users\\keerthana\\AppData\\Local\\Temp\\1\\openpyxl.02wzledt')
        df = pd.read_excel('Final_op.xlsx')
        for i in df['Agent_url'][100]:
            yield ( scrapy.Request(url=i,callback=self.parse,headers= {
                'user_agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
            }))

    
    def parse(self, response):
        yield{
                        'agent_url': response.request.url,
                        'agent_DP': response.xpath('//div[@class="col md:max-w-1/2 lg:max-w-full"]/img/@src').get(default = ""),
                        'agent_Name': response.xpath('normalize-space(//div[@class="noprint"]/h1/text())').get(default=""),
                        'agent_Phone': response.xpath('normalize-space((//div[@class="bio-phone mb-8 lg:mb-0"]/h4/span/a/text())[1])').get(default = ""),
                        'other_phone': response.xpath('normalize-space((//div[@class="bio-phone mb-8 lg:mb-0"]/h4/span/a/text())[2])').get(default = "") + str(response.xpath('normalize-space((//div[@class="bio-phone mb-8 lg:mb-0"]/h4/span/a/text())[3])').get(default = "")),
                        #'Agent_Phone3': response.xpath('normalize-space((//div[@class="bio-phone mb-8 lg:mb-0"]/h4/span/a/text())[3])').get(default = ""),
                        'Agent_Role': response.xpath('normalize-space(//div[@class="mt-2"]/h6/span/text())').get(default = ""),
                        'agent_license': response.xpath('normalize-space(//div[@class="mt-2"]/h6/span[2]/text())').get(default = ""),
                        'Agent_Designations': response.xpath('(//div[@class="col md:max-w-1/2 lg:max-w-full"])[2]').get(default=""),
                        'Agent_Facebook': response.xpath('//div[@class="mb-12"]/a[@aria-label="RE/MAX on FACEBOOK"]/@href').get(default=""),
                        'Agent_Linkedin':response.xpath('//div[@class="mb-12"]/a[@aria-label="RE/MAX on LINKEDIN"]/@href').get(default=""),
                        'Agent_instagram': response.xpath('//div[@class="mb-12"]/a[@aria-label="RE/MAX on INSTAGRAM"]/@href').get(default=""),
                        'Agent_website': response.xpath('//div[@class="w-full"]/a/@href').get(default=""),
                        'About': response.xpath('normalize-space((//div[@class="row"])[2])').extract(),
                        'Office_address': response.xpath('normalize-space(//a[@class="inline-block directions-link"])').extract_first(default=""),
                        'office_Name': response.xpath('normalize-space(//h4[@class="mb-2"]/a/text())').get(default=""),
                        'Office_Website': 'https://www.remax.com/'+str(response.xpath('//h4[@class="mb-2"]/a/@href').get(default="")),
                        # 'About': response.xpath('(//div[@class="row"])[2]/text()').extract(default="")


                    }

        