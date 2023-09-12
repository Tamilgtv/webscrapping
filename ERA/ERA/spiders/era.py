import scrapy
import requests
from bs4 import BeautifulSoup 
import pandas as pd
from ..items import EraItem

            
class EraSpider(scrapy.Spider):
    name = 'era'
    allowed_domains = ['era.com']
    start_urls = ['http://era.com/']
    
    
    

    def parse(self, response):
                    
        State=[]
        office_links=[]
        r=requests.get('https://www.era.com/real-estate-agents?companyId=reset')
        soup=BeautifulSoup(r.text)
        for i in soup.findAll('li',{'class','areaListCol'}):
            State.append('https://www.era.com'+i.a.get('href'))
        for i in State[:2]:
            r=requests.get(i)
            soup=BeautifulSoup(r.text)
            for i in soup.findAll('div',{'class','l-grid__col l-grid__col-2-3'}):
                for x in i.findAll('a'):
                    office_links.append('https://www.era.com'+x.get('href'))
                    
                    
                    
        agent_profile_url=[]
        agent_name=[]
        phone=[]
        tag=[]
        area_served=[]
        rating=[]
        office=[]
        branch=[]
        agent_facebook=[]
        agent_Youtube=[] 
        agent_Twitter=[] 
        agent_Linkedin=[] 
        agent_Instagram=[]
        agent_Yelp=[]
        state=[]
        Zip=[]
        address=[]
        office_phone=[]
        area_server=[]
        
        
        
        for url in office_links:
            r=requests.get(url)
            soup=BeautifulSoup(r.text)
            try:
                tag.append(soup.find('span',{'class':'ribbon__txt'}))
            except:
                tag.append('')
            try:
                agent_name.append(soup.find('h1',{'class':'heading-std heading-std--large mb-0'}).text)
            except:
                agent_name.append('')
            try:
                phone.append(soup.find('div',{'class':'agent-info-cont__agent-phone'}).text.strip())
            except:
                phone.append('')
            try:
                rating.append(soup.find('div',{'id':'star-ratings'}).span.text.strip())
            except:
                rating.append('')
            try:
                agent_profile_url.append(soup.find('div',{'class':'media__img media__img--agent-photo media__agent'}).img.get('src'))
                agent_dp = soup.find('div',{'class':'media__img media__img--agent-photo media__agent'}).img.get('src')
            except:
                agent_dp = ''
                agent_profile_url.append('')
            try:
                area_served.append(soup.find('div',{'class':'l-two-col-right'}).text.replace('\n\n',''))
            except:
                area_served.append('')
            try:
                office.append(soup.find('div',{'class':'l-two-col-main'}).findAll('li')[1])
            except:
                office.append('')
            try:
                branch.append(soup.find('div',{'class':'l-two-col-main'}).findAll('li')[-1])
            except:
                branch.append('')
        
            F,Y,Ye,T,L,P,I=0,0,0,0,0,0,0
            for i in soup.find('ul',{'class':'hide-bullet social-list'}).findAll('li'):
                if 'Facebook' in i.a.get('aria-label'):
                    agent_facebook.append(i.a.get('href'))
                    F=1
                if 'Linkedin' in i.a.get('aria-label'):
                    agent_Linkedin.append(i.a.get('href'))
                    L=1
                if 'Yelp' in i.a.get('aria-label'):
                    agent_Yelp.append(i.a.get('href'))
                    Ye=1
                if 'Pinterest' in i.a.get('aria-label'):
                    agent_Instagram.append(i.a.get('href'))
                    I=1
            if F == 0:
                agent_facebook.append('')
            if L == 0:
                agent_Linkedin.append('')
            if Ye == 0:
                agent_Yelp.append('')
            if I == 0:
                agent_Instagram.append('')
            try:
                agent_Youtube.append(soup.find('a',{'class':'ytp-title-link yt-uix-sessionlink'}).get('href'))
            except:
                agent_Youtube.append('')
            try:
                address.append(soup.find('div',{'class':'f-left'}).find('div',{'class':'media__content'}).text.replace('\n',''))
            except:
                address.append('')
            try:
                Zip.append(str(soup.find('div',{'class':'f-left'}).find('div',{'class':'media__content'})).split('<br/>')[2].split(',')[-1].split()[-1])
            except:
                Zip.append('')
            try:
                state.append(str(soup.find('div',{'class':'f-left'}).find('div',{'class':'media__content'})).split('<br/>')[2].split(',')[-1].split()[0])
            except:
                state.append('')
            try:
                office_phone.append(soup.find('div',{'class':'f-left'}).find('strong',{'class':'vmiddle font-15 footer-bottom--phone--CA'}).text.strip().replace('.',''))
            except:
                office_phone.append('')       
            



            self.unique_id += 1
    
            item = EraItem()
            item['unique_id'] = "era_"+str(self.unique_id)
            item['agent_url'] = response.url
            item['agent_dp'] = agent_dp
            item['agent_name'] = name
            item['agent_phone'] = mobile
            item['agent_email'] = ''
            item['agent_role'] = role
            item['agent_license'] = ''
            item['agent_areaserved'] = ''
            item['agent_designations'] = role
            item['agent_facebook'] = facebook
            item['agent_instagram'] = instagram
            item['agent_twitter'] = twitter
            item['agent_linkedin'] = linkedln
            item['agent_pinterest'] = ''
            item['agent_youtube'] = youtube
            item['agent_site'] = agent_website
            item['agent_special_tag'] = ''
            item['agent_rating'] = ''
            item['office_address'] = complete_address
            item['office_fax'] = fax
            item['office_branch'] = response.xpath("//div[@class='font-13 p-b-5']/a/text()").get(default = '')
            item['office_name'] = 'Howardhanna'
            item['office_phone'] = office_no
            item['office_site'] = response.xpath("//div[@class='font-13 p-b-5']/a/@href").get(default='')
            item['office_zip'] = office_zip
            item['office_state'] = state
            item['other_phone'] = alternate_no
            item['company_facebook'] = ''
            item['company_linkedin'] = ''
            item['company_name'] = 'ERA'
            item['company_site'] = 'https://www.era.com'
            item['company_twitter'] = ''
            item['date_of_data_extraction'] = datetime.now()
            item['data_extracted_by'] = 'Tamil'
            item['dataextraction_uuid'] = 'Tamil-'+datetime.now().strftime('%m-%d-%Y')
