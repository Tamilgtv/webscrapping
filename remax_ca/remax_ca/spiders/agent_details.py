import scrapy
import pandas as pd

class AgentDetailsSpider(scrapy.Spider):
    name = 'agent_details'
    allowed_domains = ['www.remax.ca']
    # start_urls = ['http://www.agentdetails.ca/']
    def start_requests(self):
        df = pd.read_csv(r'C:realtor_links.csv')
        url_list = df['agent_url'].to_list()
        for self.l in url_list:
            yield scrapy.Request(self.l,callback=self.parse,headers= {
                'user_agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
            })

    def parse(self, response):

        # requests =scrapy.Request(url = 'https://www.remax.ca/on/akanksha-paliwal-p102048902-ag')
        name = response.xpath('//span[@class="name-rating is-flex has-flex-align-center"]/h1/text()').get()
        try:
            role = response.xpath('//h5[@id="profileHeader-text-description"]/text()').get()
        except:
            pass
        #phone numbers and designation
        
        fast_facts = response.xpath('//div[@class="secondary-info"]/app-detail-section/section').get(default='  ')
        try:
            office_info= response.xpath('//div[@class="secondary-info"]/div[@class="office-information ng-star-inserted"]/a/text()').get(default='  ')
        except:
            pass
        #Address
        try:
            street = response.xpath('//div[@class="secondary-info"]/div[@class="office-information ng-star-inserted"]/div[@id="agentProfile-text-officeAddress"]/text()').get(default='  ')
            city= response.xpath('//div[@class="secondary-info"]/div[@class="office-information ng-star-inserted"]/div[@id="agentProfile-text-officeCityState"]/text()').get(default='  ')
            Zip= response.xpath('//div[@class="secondary-info"]/div[@class="office-information ng-star-inserted"]/div[@id="agentProfile-text-officePostalCodeCountry"]/text()').get(default='  ')
        except:
            pass
        #office url
        try:
            off_url= response.xpath('//a[@class="is-flex has-flex-align-center ng-star-inserted"]/@href').get(default='  ')
        except:
            pass
        
        #Agent URL
        try:
            agent_url = response.xpath('//div[@class="social-media"]/div/a/@href').get(default='   ')
        except:
            pass
        
        #****************************************Social Media Links**************************************
        try:
            fb = response.xpath('//div/div[1]/app-agent-profile/section/section[1]/div/app-connect-social-bar/div/div/div/a[1]/@href').get(default='  ')
            
        except:
            pass
        try:
            twitter =response.xpath('//div/div[1]/app-agent-profile/section/section[1]/div/app-connect-social-bar/div/div/div/a[2]/@href').get(default='   ')
        except:
            pass
        try:
            linkdin=response.xpath('//div/div[1]/app-agent-profile/section/section[1]/div/app-connect-social-bar/div/div/div/a[3]/@href').get(default='  ')
           
        except:
            pass
        #***************************************End of social Media links**********************************
        
        # AGent Ratings
        try:
            ratings = response.xpath('//span[@class="exact ng-star-inserted"]/text').get(default='   ')
        except:
            pass
        
        #Agent Image URL
        try:
            agent_DP = response.xpath('//div[@class="thumbnail"]/img/@src').get(default = '   ')
        except:
            pass
        

        yield{
            
            'Agent_Url':response.request.url,
            'Agent_DP':agent_DP,
            'Agent_Name': name,
            'Agent_Phone and Designation': fast_facts,
            'Agent_Role': role,
            'Agent_Facebook':fb,
            'Agent_Linkdin':linkdin,
            'Agent_Twitter':twitter,
            'Agent_Rating':ratings,
            'Agent_Site':agent_url,
            'Office_Address': (str(street)+str(city)+str(Zip)),
            'Office_Name':office_info,
            'Office_Site': off_url,
            'Office_zip': str(Zip[0:8])
        }
