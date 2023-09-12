from enum import unique
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re

class RealtorLinkSpider(CrawlSpider):
    name = 'realtor_link'
    allowed_domains = ['www.remax.com']
    start_urls = ['https://www.remax.com/real-estate-agents?page=1&count=100']
    
    
    # def Page_count_finder(self):
    #     yield scrapy.Request(url = )
        
    def start_requests(self):
        for i in range(1,4):
            yield ( scrapy.Request(url='https://www.remax.com/real-estate-agents?page='+str(i)+'&count=100',callback=self.parse,headers= {
                'user_agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
            }))
    
    
    def parse(self, response):
        print(response.text)
        
        for c in response.xpath('//div[@class="d-agent-card card"]'):
            
                cty=[]
                st= []
                name = c.xpath('normalize-space(.//div[@class="details"]/h4/text())').get()
                Name = (name.replace(" ","-")).lower()
                # print(Name)
                image = c.xpath('.//div[@class="imageContainer"]/img/@src').get()
                unique_Id = re.findall('\d{9}',image)
                data = c.xpath('normalize-space(.//script[@type="application/ld+json"]/text())').get()
                city =re.findall('"addressLocality": "(.*?)"',data)
                for c in city:
                    cty.append(c)
                state =re.findall('"addressRegion": "(.*?)"',data)
                for s in state:
                    st.append(s)
                cty_state = str(str(cty[0]).replace(" ","-")+'-'+str(st[0])+'/'+str(unique_Id).replace("['","").replace("']","")).lower()
                # print(cty_state)
                print("*************************"+name+"********************************")  
                yield{
                        'Name': name,
                        #'unique_realtor_link':'https://www.remax.com/real-estate-agents/'+str(Name)+"-"+str(cty_state)
                        'unique_realtor_link':'https://www.remax.com'+response.xpath('//*[@id="__layout"]/div/main/div/form/div/div[2]/div[2]/div/div[1]/div[2]/div[1]/a/@href').get()
                        
                        }