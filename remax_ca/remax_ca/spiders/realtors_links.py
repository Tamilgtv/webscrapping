import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import pandas as pd
from time import sleep
from scrapy.utils.response import open_in_browser

class RealtorsLinksSpider(CrawlSpider):
    name = 'realtors_links'
    # allowed_domains = ['remax.ca']
    # start_urls = ['https://www.remax.ca/real-estate-agents-in-canada']
    def start_requests(self):
        office_url = pd.read_csv('office_links_2.csv') #reading Office link 
        url_list = office_url['links'].to_list()
        yield scrapy.Request(url='https://www.remax.ca/on/stoney-creek-real-estate-agents', callback=self.parse,headers= {
                'user_agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
            })        
        # for i in url_list:
        #     yield scrapy.Request(i, callback=self.parse,headers= {
        #         'user_agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
            # })        
    def parse(self, response):
        # sleep(2)
        url = response.xpath('//div[@class="name-rating is-flex has-flex-align-center"]/a')
       
        #Extracting agent URL
        for link in url:
            yield{
            'agent_url': 'https://www.remax.ca'+str(link.xpath('.//@href').get())         
            }
        # sleep(2)
        
        # pagination 
        next_page = response.xpath('(//a[@class="pagination-item text-center ng-star-inserted"])[ last()-1]/@href').get()
        last_page = response.xpath('(//a[@class="pagination-item text-center selected ng-star-inserted"])[ last()]/text()').get()
        paginate =response.xpath('/html/body/app-root/div/div[1]/app-search-page/section/div[4]/app-gallery-view/section/div[2]/div/app-pagination/div/a[4]/text()').get()
        if  next_page:
            # sleep(2)
            yield scrapy.Request(url='https://www.remax.ca'+str(next_page ),callback = self.parse,headers= {
                'user_agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
            })        