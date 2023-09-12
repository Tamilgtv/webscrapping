import scrapy
from bs4 import BeautifulSoup
from datetime import datetime
from ..items import RoyallepageCaItem

class RoyallepageSpider(scrapy.Spider):
    name = 'royallepage'
    allowed_domains = ['royallepage.ca']
    #start_urls = ['https://www.royallepage.ca/en/search/agents/?redirect=1&address_type=true&lang=en-ca']
    start_urls = ['https://www.royallepage.ca/en/search/agents/?csrfmiddlewaretoken=eKcO3JTCbMNY8yx7iDW5VEolQFniNcECKdXj3grJZFc21oYkg2Zr38vmK5rM9oD9&lat=43.648690000000045&lng=-79.38543999999996&address=&designations=&address_type=city&city_name=&prov_code=ON&sortby=&transactionType=AGENT&name=&location=&language=&specialization=All']
    def __init__(self):
        self.unique_id  = 0
    
    def parse(self, response):

        
        yield from response.follow_all(response.xpath('//div[@class="agent-info"]/a/@href'),callback = self.parse_agent)
    

        
        next = response.xpath('//a[@class="paginator__button next button button--circle button--icon-only button--has-icon  js-paginator-button"]/@href')
        if next:
            yield from  response.follow_all(
                response.xpath('//a[@class="paginator__button next button button--circle button--icon-only button--has-icon  js-paginator-button"]/@href'),
                callback=self.parse)
            

        

    
    def parse_agent(self,response):
        soup  = BeautifulSoup(response.text, 'html.parser')
        agent_name = response.xpath("//h1[@class='media__title u-no-margins']/text()").get(default='')
        agent_dp = response.xpath("//figure[@class='image-holder-agent card__media card__media--transparent card__media--height']/img/@src").get(default='')
       
        agent_email = ''
        agent_areaserved = ''
        agent_role = response.xpath("//span[@class='media__sub-title']/text()").get(default='')
        try:
            office_name = soup.find('span',{'class':'agent-info__brokerage'}).find('a').text.strip()
        except:
            office_name = ''
        office_site = response.xpath("//span[@class='agent-info__brokerage']/a/@href").get(default='')
        
        street = response.xpath("//span[@itemprop='addressLocality']/text()").get(default='')
        city_state = response.xpath("//span[@itemprop='addressLocality']/text()").get(default='')
        Zip = response.xpath("//span[@itemprop='postalCode']/text()").get(default='')
        #phone_details = response.xpath("//p[@class='col-md-1-1']/text()").getall()
        try:
            phone_details = soup.find('div',{'class':'frow u-margin-bottom'}).find_all('p',{'class':'col-md-1-1'})
        except:
            phone_details = ''
        try:
            agent_insta = ''.join([x['href'] for x in soup.find('ul',{'class':'social-list col-md-1-1'}).find_all('a') if 'insta' in x['href']])
        except:
            agent_insta = ''
            
        try:
            agent_twitter = ''.join([x['href'] for x in soup.find('ul',{'class':'social-list col-md-1-1'}).find_all('a') if 'twitter' in x['href']])
        except:
            agent_twitter = ''
            
        try:
            agent_linkedin = ''.join([x['href'] for x in soup.find('ul',{'class':'social-list col-md-1-1'}).find_all('a') if 'link' in x['href']])
        except:
            agent_linkedin = ''
        try:
            agent_facebook = ''.join([x['href'] for x in soup.find('ul',{'class':'social-list col-md-1-1'}).find_all('a') if 'face' in x['href']])
        except:
            agent_facebook = ''  
        
        try:
            state = city_state.split(',')[-1].strip()
        except:
            state = ''
        office_phone = ''
        fax = ''
        agent_phone = ''
        phone = ''
        other_phone = ''
        for phone in phone_details:
            if 'office' in phone.text.lower():
                office_phone = phone.text.lower().replace('office','').strip()
            if 'fax' in phone.text.lower():
                fax = phone.text.lower().replace('fax','').strip()
            if 'mobile' in phone.text.lower():
                agent_phone = phone.text.lower().replace('mobile','').strip()
            if 'direct' in phone.text.lower():
                other_phone = phone.text.lower().replace('direct','').strip()
        
            
        # yield {
            
        #     'agent_url': response.request.url,
        #     'agent_name': agent_name,
        #     'agent_dp':'https:'+agent_dp,
        #     'agent_phone': agent_phone,
        #     'agent_email':'',
        #     'agent_role': agent_role,
        #     'office_name': office_name,
        #     'office_site': office_site,
        #     'office_address': street +' '+city_state+' '+Zip,
        #     'office_state' : city_state.split(',')[-1],
        #     'office_zip': Zip,
        #     'office_phone': office_phone
            
        #     }
            
        
        
        self.unique_id =self.unique_id + 1
        item = RoyallepageCaItem()
        item['unique_id'] = "Royallepage_"+str(self.unique_id)
        item['agent_url'] = response.request.url
        item['agent_dp'] = 'https:'+agent_dp
        item['agent_name'] = agent_name
        item['agent_phone'] = agent_phone
        item['agent_email'] = ""
        item['agent_role'] = agent_role
        item['agent_license'] = ""
        item['agent_areaserved'] = ''
        item['agent_designations'] = ''
        item['agent_facebook'] = agent_facebook
        item['agent_instagram'] = agent_insta
        item['agent_twitter'] = agent_twitter
        item['agent_linkedin'] = agent_linkedin
        item['agent_pinterest'] = ""
        item['agent_youtube'] = ""
        item['agent_site'] = ''
        item['agent_special_tag'] = ''
        item['agent_rating'] = ''
        item['office_address'] = street +' '+city_state+' '+Zip
        item['office_fax'] = fax
        item['office_branch'] = ''
        item['office_name'] = office_name
        item['office_phone'] = office_phone
        item['office_site'] = office_site
        item['office_zip'] = Zip
        item['office_state'] = state
        item['other_phone'] = other_phone
        item['company_facebook'] = ''
        item['company_linkedin'] = ''
        item['company_name'] = 'Royallepage'
        item['company_site'] = 'https://www.royallepage.ca/'
        item['company_twitter'] = ''
        item['date_of_data_extraction'] = datetime.now()
        item['data_extracted_by'] = 'Tamil'
        item['dataextraction_uuid'] = 'Tamil-'+datetime.now().strftime('%m-%d-%Y')

        yield item
        
        
        