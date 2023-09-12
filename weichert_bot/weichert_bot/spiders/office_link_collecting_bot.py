import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re

class OfficeLinkCollectingBotSpider(CrawlSpider):
    name = 'office_link_collecting_bot'
    allowed_domains = ['www.weichert.com']
    # start_urls = ['http://www.weichert.com/']
    def start_requests(self):
        # self.url=[]
        
        yield ( scrapy.Request(url='https://www.weichert.com/agents/',callback=self.parse_url,headers= {
                'user_agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
            }))
        # for l in self.url:
        #     yield ( scrapy.Request(url='https://www.weichert.com/search/agents/AgentList.aspx?txtFirstName=&txtLastName=&OfficeNumberCSV='+str(l),callback=self.parse_links,headers= {
        #         'user_agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
        #     }))        
    def parse_url(self, response):
        uniq_id = response.xpath('//option/@value').getall()
        
        #Extracting Office link
        for link in uniq_id:
            yield{
                'Office_link':'https://www.weichert.com/search/agents/AgentList.aspx?txtFirstName=&txtLastName=&OfficeNumberCSV='+str(link)
            }
    
        

