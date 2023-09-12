import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import pandas as pd

class AgentLinksBotSpider(CrawlSpider):
    name = 'agent_links_bot'
    allowed_domains = ['www.weichert.com']
    # start_urls = ['http://www.weichert.com/']
    def start_requests(self):
        office_links = pd.read_csv('office_link_input.csv')
        for link in office_links['Office_link']:
            yield ( scrapy.Request(url=link,callback=self.parse,headers= {
                'user_agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
            }))

    def parse(self, response):
        # agent_link= response.xpath('//div[@class="agent-profile-box"]/span/a/@href').getall()
        for link in response.xpath('//div[@class="agent-card"]'):
            yield{
                "Agent_name": link.xpath('normalize-space(.//div/h5/text())').get(),
                "link":"https://www.weichert.com"+link.xpath('.//div[2]/span/a/@href').get()

            }
        
        next_page =response.xpath('//div[@class="tablePageJumpNavigation"]/a/@href').getall()
        next_10 = response.xpath('//span[@class="spanAdjoiningGroup"]/a/@href').get()
        
        #for pagination
        if  next_10:
            yield ( scrapy.Request(url='https://www.weichert.com/'+str(next_10),callback=self.parse,headers= {
                    'user_agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
                }))
            
        #for pagination
        for Next in  next_page:
            yield ( scrapy.Request(url='https://www.weichert.com/'+str(Next),callback=self.parse,headers= {
                    'user_agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
                }))
        