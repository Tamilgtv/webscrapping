# -*- coding: utf-8 -*-
import scrapy
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
from remax_ca import items 

class RemaxSpider(scrapy.Spider):
    name = 'remax'
    allowed_domains = ['remax.ca']
    #start_urls = ['http://remax.ca/']
    
    
    # with open('D:/Tamil/AIMLEAP/CBN\CBN_BOT/remax_ca_new/remax_ca/remax_ca_links.csv') as f:
    #   start_urls = [line.strip() for line in f]
    

      
    def start_requests(self):
        self.count = 0
        self.df = pd.read_csv('remax_ca_agents_links_3.csv')
        url_list = self.df['links'].to_list()
        for self.l in range(len(url_list)):
            print(self.l)
            #self.agent_phone = self.df.loc[self.l,'Agent_phone']
            yield scrapy.Request(url_list[self.l],callback=self.parse,headers= {
                'user_agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
            })

    def parse(self, response):
        item = items.RemaxCaItem()

        soup = BeautifulSoup(response.text, 'html.parser')
        self.count = self.count + 1
        #print(response.text)
        # requests =scrapy.Request(url = 'https://www.remax.ca/on/akanksha-paliwal-p102048902-ag')
        name = response.xpath('//*[@class="agentId_summaryRoot__3L5HF"]/h1/text()').get(default= '-')
        
        try:
            role = response.xpath('//*[@class="agent-summary_title__18zd_"]/text()').get(default='-')
        except:
            role = ''
            pass
        #phone numbers and designation
        
        fast_facts = response.xpath('//div[@class="secondary-info"]/app-detail-section/section').get(default='-')
        try:
            office_info= response.xpath('//*[@class="agent-office_officeLink__22-GT"]/text()').get(default='-')
        except:
            pass
        #Address
        try:
            # street = response.xpath('//div[@class="secondary-info"]/div[@class="office-information ng-star-inserted"]/div[@id="agentProfile-text-officeAddress"]/text()').get(default='  ')
            # city= response.xpath('//div[@class="secondary-info"]/div[@class="office-information ng-star-inserted"]/div[@id="agentProfile-text-officeCityState"]/text()').get(default='  ')
            # Zip= response.xpath('//div[@class="secondary-info"]/div[@class="office-information ng-star-inserted"]/div[@id="agentProfile-text-officePostalCodeCountry"]/text()').get(default='  ')
            address = soup.find('address').text
        except:
            address = '-'
            pass
        try:
            Zip =' '.join(soup.find('address').text.replace('\n',' ').split(',')[-2].strip().split(' ')[1:])
        except:
            Zip ='-'
            
        try:
            state =' '.join(soup.find('address').text.replace('\n',' ').split(',')[-2].strip().split(' ')[0])
        except:
            state = ''
        #office url
        try:
            off_url= response.xpath('//*[@class="agent-office_officeLink__22-GT"]/@href').get(default='-')
        except:
            pass
        
        #Agent URL
        try:
            agent_url = ''.join([x['href'] for x in soup.find_all('a',{'class':'agent-links_socialLink__1iRGm'}) if 'website' in x['aria-label'].lower()])
        except:
            agent_url = ''
            pass
        
        #****************************************Social Media Links**************************************
        try:
            #fb = response.xpath('//*[@class="agent-links_socialLink__1iRGm"]/@href').get(default='  ')
            fb  = ''.join([x['href'] for x in soup.find_all('a',{'class':'agent-links_socialLink__1iRGm'}) if 'face' in x['href']])
            
        except:
            fb = '-'
            pass
        try:
            twitter =''.join([x['href'] for x in soup.find_all('a',{'class':'agent-links_socialLink__1iRGm'}) if 'twitter' in x['href']])
        except:
            twitter = '-'
            pass
        try:
            linkdin =''.join([x['href'] for x in soup.find_all('a',{'class':'agent-links_socialLink__1iRGm'}) if 'linkedin' in x['href']])
           
        except:
            linkdin = '-'
            pass
        
        try:
            insta =''.join([x['href'] for x in soup.find_all('a',{'class':'agent-links_socialLink__1iRGm'}) if 'insta' in x['href']])
           
        except:
            insta = '-'
            pass
        #***************************************End of social Media links**********************************
        
        # AGent Ratings
        try:
            ratings = response.xpath('//span[@class="exact ng-star-inserted"]/text()').get(default='-')
        except:
            pass
        
        #Agent Image URL
        try:
            agent_DP = response.xpath('//*[@class="agent-summary_imageCtaWrapper__2gA-3"]/div/img/@src').get(default = '-')
        except:
            pass
        
        
        count = 0
        num = []
        for  i in soup.find_all('script'):
            if 'telephone' in str(i):
                for j in str(i).split(','):
                    if 'telephone' in j:
                        count = count+1
                        num.append(j.replace('}]}</script>','').replace('"telephone":','').replace('"','').replace('-',''))
                        print(j.replace('}]}</script>','').replace('"telephone":','').replace('"',''))
        
        if len(num) > 1:
            Agent_phone = num[0]
            office_phone = num[1]
        else:
            Agent_phone = num[0]
            
            
            
        # yield{
            
        #     'Agent_Url':response.request.url,
        #     'Agent_DP':agent_DP,
        #     'Agent_Name': name,
        #     'Agent_phone': Agent_phone ,
        #     'Designation': fast_facts,
        #     'Agent_Role': role,
        #     'Agent_Facebook':fb,
        #     'Agent_Linkdin':linkdin,
        #     'Agent_Twitter':twitter,
        #     'Agent_Rating':ratings,
        #     'Agent_Site':agent_url,
        #     'Office_Address': address,
        #     'office_phone' : office_phone,
        #     'Office_Name':office_info,
        #     'Office_Site': off_url,
        #     'Office_zip': Zip
            
        #    }



        item['unique_id'] = 'Remax_ca_'+str(self.count)
        item['agent_url'] = response.request.url
        item['agent_dp'] = agent_DP
        item['agent_name'] = name
        item['agent_phone'] = Agent_phone.replace('Mobile:','').replace('Direct:','').replace('-','').replace('(','').replace(')','').replace(' ','')
        item['agent_email'] = ''
        item['agent_role'] = role
        item['agent_license'] = ''
        item['agent_areaserved'] = ''
        item['agent_designations'] = fast_facts
        item['agent_facebook'] = fb
        item['agent_instagram'] = insta
        item['agent_twitter'] = twitter
        item['agent_linkedin'] = linkdin
        item['agent_pinterest'] = ''
        item['agent_youtube'] = ''
        item['agent_site'] = agent_url
        item['agent_special_tag'] = ''
        item['agent_rating'] = ratings
        item['office_address'] = address
        item['office_fax'] = '' 
        item['office_branch'] = ''
        item['office_name'] = office_info
        item['office_phone'] = office_phone
        item['office_site'] = off_url
        item['office_zip'] = Zip
        item['office_state'] = state
        item['other_phone'] = ''
        item['company_facebook'] = ''
        item['company_linkedin'] = ''
        item['company_name'] = 'Remax'
        item['company_site'] = 'https://www.remax.ca/'
        item['company_twitter'] = ''
        item['date_of_data_extraction'] = datetime.now()
        item['data_extracted_by'] = 'Tamil'
        item['dataextraction_uuid'] = 'Tamil-'+datetime.now().strftime('%m-%d-%Y')

        yield item