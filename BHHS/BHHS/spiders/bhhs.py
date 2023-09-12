# -*- coding: utf-8 -*-
import scrapy
import re
from bs4 import BeautifulSoup
from ..items import BhhsItem
from datetime import datetime 
import pandas as pd
df = pd.read_csv('office_info.csv')

def office_details(address):
    office_de = df[df['address']==address]
    
    office_de.reset_index(drop = True, inplace = True)
    
    try:
        office_site = office_de.loc[0,'office_site']
        office_phone = office_de.loc[0,'office_phone']
        fax = office_de.loc[0,'fax']
    except:
        office_site = ''
        office_phone = ''
        fax = ''
        
    return office_site, office_phone , fax 
    


class BhhsSpider(scrapy.Spider):
    name = 'bhhs'
    allowed_domains = ['www.bhhs.com']
    #start_urls = ['https://www.bhhs.com/fox-and-roach-realtors-pa301/margate-city/james-abbott/cid-1035574']
    #with open('D:/Tamil/AIMLEAP/CBN/CBN_BOT/BHHS/bhhs_agents_links.csv') as f:
          #start_urls = [line.strip() for line in f]
          
    agent_links = pd.read_csv('bhhs_agents_links.csv')
    start_urls = agent_links['agent_links'].to_list()

    def __init__(self):
        
        self.unique_id = 0
        
    def parse(self, response):
        
        
        soup = BeautifulSoup(response.text,'html.parser')
        # languages= list(filter(None, [
        #             text.get().replace('\n', '').strip("<li>").strip("</")
        #             for text in
        #             response.xpath('//*[@id="languages"]/li')
        #         ]))[0:6]
        off_add = ''.join([x.replace('                            ',' ') for x in soup.find('div',{'class':'cmp-agent__office'}).text.splitlines()[-3:-1]]).strip()
        
        
        off_site , offph , fax = office_details(off_add)
        
        fax=response.xpath("(//div[@class='cmp-agent-details details row']/ul/li/em/text())[3]").get(default = "-")
        number = response.xpath("(//div[@class='cmp-agent-details details row']/ul/li/em/text())[2]").get(default = "-")
        #offnum = response.css("li:nth-child(1) .cmp-agent-details__phone-number::text").get(default = "-")
        offnum = soup.find('div',{'class':'cmp-footer-franchisee__franchiseeDetails'}).find('p').text.split('\n')[-3].strip().replace(',','')
        #offnum = offnum.split(' ')[-1].strip().replace(',','')
        
        print('**************office number***************')
        print(offnum)
        Agent_no = response.xpath("//div[@class='cmp-agent-details details row']/ul/li/a/text()").get(default ="-")
        Agent_dp = response.xpath("//meta[@property='og:image']/@content").get(default ="-")
        name = response.css(".homepage_link::text").get(default ="-")
        # address = list(filter(None, [
        #             text.get().replace('\n', '').strip("")
        #             for text in
        #             response.css('.cmp-agent__office::text')
        #         ]))[0:6]
        address = (str(response.css('.cmp-agent__office::text').get()).strip()).split("\n")
        print(address)
        print("????????????????????????????"+str(len(address))+"-----????????????////////////////////")
        special_tag = response.css("#accreditations li::text").get(default ="-")
        agent_license = response.xpath("//ul[@class='cmp-agent-details__license text-uppercase d-flex flex-column flex-lg-row flex-wrap']/@data-license").get(default ="-")
        agent_site = response.css(".cmp-agent-details__website::text").get(default ="-")
        about = response.css("#biotxt::text").get(default ="-")
        email = response.xpath("//*[@class='cmp-agent-details__mail text-lowercase']/@href").get(default ="-")
        role = response.css(".cmp-agent__title::text").get(default ="-")
        num = []
        if number == "mobile":
            num.append(Agent_no)
            P_type = "mobile"
        else:
            num.append(Agent_no)
            P_type = "-"
        offfax = response.xpath("//*[@id='pageAgentDetail-e7d87cbd0b']/div[1]/div/div/div/div[3]/div/div/section/div[1]/div[1]/div[2]/div[1]/ul/li[3]/a/text()").get(default = "-")
        faxno = []
        if fax == "fax":
            faxno.append(offfax)

        fb = response.css("a[target='_blank'][href*='facebook.com']::attr(href)").get(default ="-")
        tw = response.css("a[target='_blank'][href*='twitter.com']::attr(href)").get(default ="-")
        insta = response.css("a[target='_blank'][href*='instagram.com']::attr(href)").get(default ="-")
        yout = response.css("a[target='_blank'][href*='youtube.com']::attr(href)").get(default ="-")
        lin = response.css("a[target='_blank'][href*='linkedin.com']::attr(href)").get(default ="-")
        
        #zip ="["+ str(re.findall('\d{5}(?:[-\s]\d{4})?$',response.xpath('normalize-space((//*[@class="media__content"]/text()[3])[2])').get(default='-')))+"]"
        # yield{
        #     'Agent_URL': response.url,
        #     'Agent_DP': Agent_dp,
        #     'Agent_Name': name,
        #     'Agent_Phone':num,
        #     'Phone_type':P_type,
        #     'Agent_Email':str(email).replace('mailto:','').replace('[','').replace(']',''),
        #     'Agent_Role':role,
        #     'Agent_License':agent_license,
        #     'Agent_AreaServed': '-',
        #     'Agent_Designation': role,
        #     'Agent_bio': about,
        #     'Agent_Language':'',
        #     'Agent_Facebook':fb,
        #     'Agent_Linkedin':lin,
        #     'Agent_Instagram':insta,
        #     'Agent_Twitter':tw,
        #     'Agent_Pinterest':"-",
        #     'Agent_Youtube':yout,
        #     'Agent_Site':agent_site,
        #     'Agent_Special_Tag':special_tag,
        #     'Agent_Rating':"-",
        #     'Office_Address':(str(address[2])+","+str(address[3]).strip()).strip(),
        #     'Office_Fax':faxno,
        #     'Office_Branch':(str(address[0])+","+str(address[1].strip())).strip(),
        #     'Office_Phone':offnum,
        #     'office_site':"-",
        #     'office_Zip':str(re.findall('\d{5}(?:[-\s]\d{4})?$',str(address[-1]).strip())),
        
        #     'Other_phone':'-',
        #     'Company_Facebook':"-",
        #     'Company_Linkedin':"-",
        #     'Company_Name':"Berkshire Hathaway HomeServices",
        #     'Company_site':"https://www.bhhs.com/",
        #     'Company_Twitter':"-" }
        
        
        self.unique_id += 1

        item = BhhsItem()
        item['unique_id'] = "Bhhs_"+str(self.unique_id)
        item['agent_url'] = response.url
        item['agent_dp'] = Agent_dp
        item['agent_name'] = name
        item['agent_phone'] = Agent_no
        item['agent_email'] = str(email).replace('mailto:','').replace('[','').replace(']','')
        item['agent_role'] = role
        item['agent_license'] = agent_license
        item['agent_areaserved'] = ''
        item['agent_designations'] = role
        item['agent_facebook'] = fb
        item['agent_instagram'] = insta
        item['agent_twitter'] = tw
        item['agent_linkedin'] = lin
        item['agent_pinterest'] = ''
        item['agent_youtube'] = yout
        item['agent_site'] = agent_site
        item['agent_special_tag'] = special_tag
        item['agent_rating'] = ''
        item['office_address'] = off_add
        item['office_fax'] = fax
        item['office_branch'] = (str(address[0])+","+str(address[1].strip())).strip()
        item['office_name'] = (str(address[0])+","+str(address[1].strip())).strip()
        item['office_phone'] = offph
        item['office_site'] = off_site
        item['office_zip'] = off_add.split(' ')[-1]
        item['office_state'] = off_add.split(' ')[-2]
        item['other_phone'] = ''
        item['company_facebook'] = ''
        item['company_linkedin'] = ''
        item['company_name'] = 'Berkshire Hathaway HomeServices'
        item['company_site'] = 'https://www.bhhs.com/'
        item['company_twitter'] = ''
        item['date_of_data_extraction'] = datetime.now()
        item['data_extracted_by'] = 'Tamil'
        item['dataextraction_uuid'] = 'Tamil-'+datetime.now().strftime('%m-%d-%Y')

        yield item

