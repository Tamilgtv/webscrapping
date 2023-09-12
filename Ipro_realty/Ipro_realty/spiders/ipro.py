import scrapy
from bs4 import BeautifulSoup
import pandas as pd

class IproSpider(scrapy.Spider):
    name = 'ipro'
    allowed_domains = ['iprorealty.com']
    start_urls = ['https://www.iprorealty.com/agent_find?country=&county=&city=&title=&brID1=&brID2=&brokerID=&brokerID_additional=&language=&first_ajax=&first_or_last=1&last_ajax=']
    
    def __init__(self):
        
        self.df = pd.DataFrame([])
        self.z = 0        
        self.unique_id = 0
        
    def parse(self, response):
        
        soup = BeautifulSoup(response.text , 'html.parser')
        
        for agent_detail in soup.find_all('div',{'class':'agent-summary-wrapper'}):
            try:
                agent_url = 'https://www.iprorealty.com'+agent_detail.find('a')['href']
            except:
                agent_url = ''
            try:
                agent_name = agent_detail.find('h3',{'class':'agent-name'}).text
            except:
                agent_name = ''
            try:
                agent_dp = 'https://www.iprorealty.com'+agent_detail.find('img')['src']
            except:
                agent_dp = ''
            try:
                agent_role = agent_detail.find('h4',{'class':'agent_title'}).text
            except:
                agent_role = ''
            try:
                agent_mobile = agent_detail.find('a',{'class':'mobile-phone-link'})['href'].replace('tel:','').replace('Direct','').strip() #agent_mobile
            except:
                agent_mobile = ''
            try:
                agent_site = agent_detail.find('a',{'class':'agent-site-link'})['href']
            except:
                agent_site = ''
            try:
                office_phone = agent_detail.find('a',{'class':'office-phone-link'})['href'].replace('tel:','')
            except:
                office_phone = ''
            try:
                office_name = 'iPro Realty Ltd., Brokerage'
            except:
                office_name = ''
            try:
                office_address = agent_detail.find('span',{'class':'brokerage-information contact-data'}).text
            except:
                office_address = ''
                
            
            self.df.loc[self.z,'agent_url'] = agent_url
            self.df.loc[self.z,'agent_dp'] = agent_dp
            self.df.loc[self.z,'agent_name'] = agent_name
            self.df.loc[self.z,'agent_role'] = agent_role
            self.df.loc[self.z,'agent_mobile'] = agent_mobile
            self.df.loc[self.z,'agent_site'] = agent_site
            self.df.loc[self.z,'office_phone'] = office_phone
            self.df.loc[self.z,'office_name'] = office_name
            self.df.loc[self.z,'office_address'] = office_address
            self.z = self.z+1    
            
            self.df.to_csv('ipro_realty.csv', index = False)

        if self.z < 100:  
            yield from response.follow_all(response.xpath('//a[@class="pager-next active"]'), callback=self.parse)
               
            
           
