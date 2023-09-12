######## this code will collect information from all the links ######


import scrapy
from datetime import datetime
from ..items import C21Item
import pandas as pd

class AgentsSpider(scrapy.Spider):
    name = 'agents'
    
    df = pd.read_csv('agent_ca_links.csv')
    
    start_urls = list(set(df['links'].to_list()))
# Here we are reading the agent links file
    # with open('agent_links.txt') as f:
    #     start_urls = [line.strip() for line in f]

# Here we are parsing each Agent Link to collect Information

    def __init__(self):
        
        self.unique_id = 21240
        

    def parse(self, response):

        address = list(filter(None, [
                text.get().replace('\n', '').strip()
                for text in
                response.css('div[class="aos-agent-office-meta-detail margin-left-right-streach-15"] ::text')
            ]))[0:5]
        zipcode = response.xpath("//*[@class='aos-agent-office-location-city-state-zip']/text()").get()
        
        try:
            add = response.xpath("//*[@class='aos-agent-office-location-address-1']/text()").get()+' '+zipcode
        except:
            add = address
        try:
            state = zipcode[-10:].strip().split(' ')[0]
            
            Zip = zipcode[-10:].strip().split(' ')[1]
        except:
            state = ''
            Zip = ''
        # yield {
        #     'Agent_URL' : response.url,
        #      'Agent_DP' :response.xpath("//*[@class='aos-agent-image']/img/@src").get(),
        #     'Agent_Name' :response.css("h1.aos-agent-display-name::text").get().split(),

        #     'Agent_Main' :response.xpath("//*[contains(text(),'Main')]/following-sibling::a/text()").get(),
        #     'Agent_Cell': response.xpath("//*[contains(text(),'Cell')]/following-sibling::a/text()").get(),
        #     'Agent_Office': response.xpath("//*[contains(text(),'Office')]/following-sibling::a/text()").get(),
        #     'Agent_Email' : response.xpath("//*[contains(text(),'Email')]/following-sibling::a/text()").get(),
        #     'Agent_Role' : response.css("div.aos-agent-licensing-info p::text").get(),

        #     'Agent_Designation': response.css(".aos-agent-licensing-info p+ p::text").get(),
        #     'Agent_Facebook':
        #         response.css(".aos-agent-social-media-icon-facebook::attr(href)").extract(),
        #     'Agent_Linkedln':
        #         response.css(".aos-agent-social-media-icon-linkedin::attr(href)").get(),
        #     'Agent_Instagram':
        #         response.css(".aos-agent-social-media-icon-instagram::attr(href)").get(),
        #     'Agent_Twitter':
        #         response.xpath("//*[@class=' aos-agent-social-media-icon-twitter']/@href").get(),

        #     'Company_Site': response.xpath("//*[contains(text(),'Website')]/following-sibling::a/text()").get(),
        #     'Office_Name': response.css(".aos-agent-office-display-name a::text").get(),
        #     'Office_Address': address,
        #     'Office_Zip': zipcode[-10:]
        # }

        self.unique_id += 1

        item = C21Item()
        item['unique_id'] = "Century21_ca_"+str(self.unique_id)
        item['agent_url'] = response.url
        item['agent_dp'] = response.xpath("//*[@class='aos-agent-image']/img/@src").get()
        item['agent_name'] = response.css("h1.aos-agent-display-name::text").get().replace('\n','').strip()
        item['agent_phone'] = response.xpath("//*[contains(text(),'Cell')]/following-sibling::a/text()").get()
        item['agent_email'] = response.xpath("//*[contains(text(),'Email')]/following-sibling::a/text()").get()
        item['agent_role'] = response.css("div.aos-agent-licensing-info p::text").get()
        item['agent_license'] = ''
        item['agent_areaserved'] = ''
        item['agent_designations'] = response.css(".aos-agent-licensing-info p+ p::text").get()
        item['agent_facebook'] = response.css(".aos-agent-social-media-icon-facebook::attr(href)").get()
        item['agent_instagram'] = response.css(".aos-agent-social-media-icon-instagram::attr(href)").get()
        item['agent_twitter'] = response.xpath("//*[@class=' aos-agent-social-media-icon-twitter']/@href").get()
        item['agent_linkedin'] = response.css(".aos-agent-social-media-icon-linkedin::attr(href)").get()
        item['agent_pinterest'] = ''
        item['agent_youtube'] = ''
        item['agent_site'] = response.xpath("//*[contains(text(),'Website')]/following-sibling::a/text()").get()
        item['agent_special_tag'] = ''
        item['agent_rating'] = ''
        item['office_address'] = add
        item['office_fax'] = ''
        item['office_branch'] = ''
        item['office_name'] = response.css(".aos-agent-office-display-name a::text").get()
        item['office_phone'] = response.xpath("//*[contains(text(),'Office')]/following-sibling::a/text()").get()
        item['office_site'] = ''
        item['office_zip'] = Zip
        item['office_state'] = state
        item['other_phone'] = response.xpath("//*[contains(text(),'Main')]/following-sibling::a/text()").get()
        item['company_facebook'] = ''
        item['company_linkedin'] = ''
        item['company_name'] = 'Century21'
        item['company_site'] = 'https://www.c21.ca'
        item['company_twitter'] = ''
        item['date_of_data_extraction'] = datetime.now()
        item['data_extracted_by'] = 'Tamil'
        item['dataextraction_uuid'] = 'Tamil-'+datetime.now().strftime('%m-%d-%Y')

        yield item
