import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re
import pandas as pd
from weichert_bot import items
from datetime import datetime


class AgentDetailsCollectorSpider(CrawlSpider):
    name = 'agent_details_collector'
    allowed_domains = ['www.weichert.com']
    start_urls = ['https://www.weichert.com/search/agents/AgentProfile.aspx?site=wdc&agent=F3858&office=50-N25']
    
    def start_requests(self):
        agent_details=pd.read_csv('agent_input_links_2.csv')
        self.count = 0
        for link in agent_details['link']:
            yield scrapy.Request(url=link, callback=self.parse,headers= {
                'user_agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
            })
    def parse(self, response):
        item = items.WeichertBotItem()
        self.count = self.count + 1
        #for collecting personal phone numbers of agent
        try:
            if response.xpath('//a[contains(text(),"Phone:")]').get():
                phone = (response.xpath('normalize-space(//a[contains(text(),"Phone:")]/text())').get(default="")).replace('Phone:',"")
            elif response.xpath('//span[contains(text(),"Mobile:")]').get():
                phone = (response.xpath('normalize-space(//span[contains(text(),"Mobile:")])').get(default="")).replace("Mobile:","").replace('\xa0',"")
            elif response.xpath('//span[contains(text(),"DIRECT:")]').get():
                phone = (response.xpath('normalize-space(//span[contains(text(),"DIRECT:")])').get(default="")).replace("DIRECT:","").replace('\xa0',"")
            else:
                phone=""
        except:
            pass
        
        #conditions for collecting office_phone_number
        try:
            if response.xpath('//a[contains(text(),"Office:")]').get():
                office_phone = (response.xpath('normalize-space(//a[contains(text(),"Office:")]/text())').get(default="")).replace("Office:","")
            elif response.xpath('//span[contains(text(),"Office: ")]').get():
                office_phone = (response.xpath('normalize-space(//span[contains(text(),"Office: ")]/text())').get(default="")).replace("Office: ","")
            else:
                office_phone=""
        except:
            pass

        zip_code =response.xpath('normalize-space(//span[@id="ctl00_BodyContent_lblCityStateZip"]/text())').get(default="")
        #applying regex for seperating zipcode from state
        Zip = re.findall('\d{5}',zip_code) 
        Zip =  str(''.join(filter(str.isdigit, Zip)))
               
        #for collecting "About_agent" information
        try:
            if response.xpath('//div[@style="margin:20px 0"]').get():
                About_agent = response.xpath('normalize-space(//div[@style="margin:20px 0"])').get(default="")
            elif response.xpath('//div[@style="margin:20px 0;"]').get():
                About_agent=response.xpath('normalize-space(//div[@style="margin:20px 0;"])').get(default="")
            else:
                About_agent= ""
        except:
            pass
        
        Address = response.xpath('normalize-space(//span[@id="ctl00_BodyContent_lblAddress"]/text())').get(default="")+','+str(response.xpath('normalize-space(//span[@id="ctl00_BodyContent_lblCityStateZip"]/text())').get(default=""))
        state = Address.split(' ')[-2]
        #yield{
            
            
            # 'Agent_Url': response.request.url,
            # 'Agent_DP': response.xpath('//div[@id="ctl00_BodyContent_ImageSection"]/img/@src').get(default=""),
            # 'Agent_Name': response.xpath('normalize-space((//div[@class="col-sm-12 col-md-10"]/div/span)[1]/text())').get(default=""),
            # 'Agent_Phone': phone,
            # 'Agent_Fax': (response.xpath('normalize-space(//span[@id="ctl00_BodyContent_lblFax"]/text())').get(default="")).replace("Fax: ",""),
            # 'Agent_Email':(response.xpath('normalize-space(//span[@id="ctl00_BodyContent_lblEmail"]/text())').get(default="")),
            # 'Agent_Website':response.xpath('//a[@id="ctl00_BodyContent_AgentWebSite"]/@href').get(default=""),
            # 'About_Agent':About_agent,
            # 'Office_Address':(response.xpath('normalize-space(//span[@id="ctl00_BodyContent_lblAddress"]/text())').get(default="")+','+str(response.xpath('normalize-space(//span[@id="ctl00_BodyContent_lblCityStateZip"]/text())').get(default=""))),
            # 'Office_Name':(response.xpath('normalize-space(//span[@id="ctl00_BodyContent_lblOfficeName"]/text())').get(default="")),
            # 'Office_Phone':office_phone,
            # 'office_Zip':Zip

            #}
            
        item['unique_id'] = 'Weichert_'+str(self.count)
        item['agent_url'] = response.request.url
        item['agent_dp'] = response.xpath('//div[@id="ctl00_BodyContent_ImageSection"]/img/@src').get(default="")
        item['agent_name'] = response.xpath('normalize-space((//div[@class="col-sm-12 col-md-10"]/div/span)[1]/text())').get(default=""),
        item['agent_phone'] = phone.replace('Mobile:','').replace('Direct:','').replace('-','').replace('(','').replace(')','').replace(' ','')
        item['agent_email'] = response.xpath('normalize-space(//span[@id="ctl00_BodyContent_lblEmail"]/text())').get(default="")
        item['agent_role'] = 'Agent'
        item['agent_license'] = ''
        item['agent_areaserved'] = ''
        item['agent_designations'] = ''
        item['agent_facebook'] = ''
        item['agent_instagram'] = ''
        item['agent_twitter'] = ''
        item['agent_linkedin'] = ''
        item['agent_pinterest'] = ''
        item['agent_youtube'] = ''
        item['agent_site'] = response.xpath('//a[@id="ctl00_BodyContent_AgentWebSite"]/@href').get(default="")
        item['agent_special_tag'] = ''
        item['agent_rating'] = ''
        item['office_address'] = response.xpath('normalize-space(//span[@id="ctl00_BodyContent_lblAddress"]/text())').get(default="")+','+str(response.xpath('normalize-space(//span[@id="ctl00_BodyContent_lblCityStateZip"]/text())').get(default=""))
        item['office_fax'] = response.xpath('normalize-space(//span[@id="ctl00_BodyContent_lblFax"]/text())').get(default="").replace("Fax: ","")
        item['office_branch'] = ''
        item['office_name'] = response.xpath('normalize-space(//span[@id="ctl00_BodyContent_lblOfficeName"]/text())').get(default="")
        item['office_phone'] = office_phone
        item['office_site'] = ''
        item['office_zip'] = Zip
        item['office_state'] = state
        item['other_phone'] = ''
        item['company_facebook'] = ''
        item['company_linkedin'] = ''
        item['company_name'] = 'Weichert'
        item['company_site'] = 'https://www.weichert.com'
        item['company_twitter'] = ''
        item['date_of_data_extraction'] = datetime.now()
        item['data_extracted_by'] = 'Tamil'
        item['dataextraction_uuid'] = 'Tamil-'+datetime.now().strftime('%m-%d-%Y')

        yield item
    

      