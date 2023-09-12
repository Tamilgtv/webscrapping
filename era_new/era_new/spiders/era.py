import scrapy
from ..items import EraNewItem
from bs4 import BeautifulSoup
from datetime import datetime

class EraSpider(scrapy.Spider):
    name = 'era'
    allowed_domains = ['era.com']
    start_urls = ['https://www.era.com/']
    
    def __init__(self):
        self.unique_id  = 0

    def parse(self, response):
        
        yield from response.follow_all(response.xpath('//li[@class="find-local-office-element"]/a/@href'),callback = self.parse_state)
        
        
    
    
    def parse_state(self, response):
        
        yield from response.follow_all(response.xpath('//th[@class="js-area-order js-list-brokerage"]/a/@href'),callback = self.parse_brokerage)
        
        
    def parse_brokerage(self, response):
        
        yield from response.follow_all(response.xpath('//div[@class="pod__office"]/h3/a/@href'),callback = self.parse_office)
        
        
    def parse_office(self, response):
        
        yield from response.follow_all(response.xpath('//a[@class="agent-link"]/@href'),callback = self.parse_agent)   
        
    def parse_agent(self, response):
        
        
        soup = BeautifulSoup(response.text, 'html.parser')
        agent_name = response.xpath('//*[@class="agent-heading"]/h1/text()').get(default='')
        agent_phone = response.xpath('//*[@class="agent-info-cont__agent-phone"]/a/text()').get(default='')
        agent_dp = response.xpath('//div[@class="media__img media__img--agent-photo media__agent"]/img/@src').get(default='')
        office_name =  response.xpath('//span[@class="mls-company-name"]/text()').get(default='')
        try:
            office_address = soup.find('div',{'class':'f-left'}).find('div',{'class':'media__content'}).text.replace('\n','')
            
        except:
            office_address = ''
            
        try:
            Zip = str(soup.find('div',{'class':'f-left'}).find('div',{'class':'media__content'})).split('<br/>')[2].split(',')[-1].split()[-1]
        except:
            Zip = ''
            
        try:
            state =str(soup.find('div',{'class':'f-left'}).find('div',{'class':'media__content'})).split('<br/>')[2].split(',')[-1].split()[0]
        except:
            state = ''
        
        try:
            office_phone = soup.find('div',{'class':'f-left'}).find('strong',{'class':'vmiddle font-15 footer-bottom--phone--CA'}).text.strip().replace('.','')
        except:
            office_phone = ''
        try:
            agent_Youtube = soup.find('a',{'class':'ytp-title-link yt-uix-sessionlink'}).get('href')
        except:
            agent_Youtube = ''
            
        try:
            rating =soup.find('div',{'id':'star-ratings'}).span.text.strip()
        except:
            rating = ''
        try:
            area_served = soup.find('div',{'class':'l-two-col-right'}).text.replace('\n\n','')
        except:
            area_served = ''
        
        try:
            branch = soup.find('div',{'class':'l-two-col-main'}).findAll('li')[-1].text
        except:
            branch = ''
        
        F,Y,Ye,T,L,P,I=0,0,0,0,0,0,0
        try:
            for i in soup.find('ul',{'class':'hide-bullet social-list'}).findAll('li'):
                if 'Facebook' in i.a.get('aria-label'):
                    agent_facebook= i.a.get('href')
                    F=1
                if 'Linkedin' in i.a.get('aria-label'):
                    agent_Linkedin = i.a.get('href')
                    L=1
                if 'Yelp' in i.a.get('aria-label'):
                    agent_Yelp = i.a.get('href')
                    Ye=1
                if 'Pinterest' in i.a.get('aria-label'):
                    agent_Instagram = i.a.get('href')
                    I=1
        except:
            pass
        if F == 0:
            agent_facebook = ''
        if L == 0:
            agent_Linkedin = ''
        if Ye == 0:
            agent_Yelp = ''
        if I == 0:
            agent_Instagram= ''
        
        
        self.unique_id =self.unique_id + 1
        item = EraNewItem()
        item['unique_id'] = "era_"+str(self.unique_id)
        item['agent_url'] = response.request.url
        item['agent_dp'] = agent_dp
        item['agent_name'] = agent_name
        item['agent_phone'] = agent_phone
        item['agent_email'] = ""
        item['agent_role'] = ''
        item['agent_license'] = ""
        item['agent_areaserved'] = area_served
        item['agent_designations'] = ''
        item['agent_facebook'] = agent_facebook
        item['agent_instagram'] = agent_Instagram
        item['agent_twitter'] = ''
        item['agent_linkedin'] = agent_Linkedin
        item['agent_pinterest'] = ""
        item['agent_youtube'] = agent_Youtube
        item['agent_site'] = ''
        item['agent_special_tag'] = ''
        item['agent_rating'] = rating
        item['office_address'] = office_address
        item['office_fax'] = ''
        item['office_branch'] = branch
        item['office_name'] = office_name
        item['office_phone'] = office_phone
        item['office_site'] = ''
        item['office_zip'] = Zip
        item['office_state'] = state
        item['other_phone'] = ''
        item['company_facebook'] = ''
        item['company_linkedin'] = ''
        item['company_name'] = 'ERA'
        item['company_site'] = 'https://www.era.com'
        item['company_twitter'] = ''
        item['date_of_data_extraction'] = datetime.now()
        item['data_extracted_by'] = 'Tamil'
        item['dataextraction_uuid'] = 'Tamil-'+datetime.now().strftime('%m-%d-%Y')

        yield item
        