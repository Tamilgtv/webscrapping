import scrapy
from scrapy import selector
from scrapy.http.response import text
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from shutil import which
# import js2xml
# import lxml.etree
# from parsel import Selector

class BhgreSpider(scrapy.Spider):
    name = 'BHGRE'
    allowed_domains = ['www.bhgre.com']
    start_urls = ['https://www.bhgre.com/']
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument('headless')
        chrome_path = which(r'/home/bharath/Desktop/phone_number_bot/chromedriver')
        self.driv = webdriver.Chrome(executable_path=chrome_path,chrome_options =chrome_options )
################################ For parsing into city#################################
    def parse(self, response):
        yield from response.follow_all(
            response.xpath('//li[@class="find-local-office-element"]/a/@href'),
        callback = self.parse_brokerage
        )
################################ For parsing into Bhgre Real Estate Brokers#################
    def parse_brokerage(self,response):
        yield from response.follow_all(
            response.xpath('//th[@class="js-area-order js-list-brokerage"]/a/@href'),
            callback = self.parse_office
        )
################################ For parsing into  Office#################################
    def parse_office(self,response):
        yield from  response.follow_all(
            response.xpath('//div[@class="pod__office"]/h3/a/@href'),
            callback = self.parse_agent
        )
################################ For parsing into Agent profile ############################
    def parse_agent(self,response):
        yield from response.follow_all(
            response.xpath('//div[@class="results-row "]/a/@href') ,
            callback=self.parse_agent_details
        )
################################ For getting agent details #################################

    def parse_agent_details(self,response):
            driver=self.driv
            driver.get(response.request.url)
            areaserved =  str(",".join([txt.strip() for txt in response.xpath('//ul[@id="all-areas-list"]/li//text()').extract()]))
            if len(areaserved)>1:
                 Agent_AreaServed = areaserved
            else:
                Agent_AreaServed = "NAN"
            # language = str(",".join([txt.strip() for txt in response.xpath('//*[ancestor::div[h2[contains(text(),"I Speak")]]]/li//text()').extract()]))
            # if len(language)>1:
            #     Agent_Language = language
            # else:
            #     Agent_Language = "NAN"
            special_tag = str("|||".join([txt.strip() for txt in response.xpath('//*[ancestor::div[h2[contains(text(),"My Credentials and Memberships")]]]/li//text()').extract()]))
            if len(special_tag)>1:
                Agent_Special_Tag = special_tag
            else:
                Agent_Special_Tag = "NAN"
            item={}
            item['Agent_url']= response.request.url
            item['Agent_DP']= response.xpath('//div[@class="media__img media__img--agent-photo media__agent"]/img/@src').get(default="")
            item['Agent_Name']=response.xpath('normalize-space(//div[@class="agent-heading"]/h1/text())').get(default="")
            item['Agent_Phone']= (response.xpath('//div[@class="agent-info-cont__agent-phone"]/a/@href').get(default="Not Found")).replace('tel:','').replace('.','')
            item['Agent_Phone_Type']="NAN"
            item['Agent_Email']=driver.find_element_by_xpath('//span[@class="profile-line agent-contact prof-wrap"]/a[@class="email"]').get_attribute('href').replace('mailto:',"")
            item['Agent_Role']='Associate Real Estate Broker'
            item['Agent_License']=(response.xpath('(//span[contains(text(),"CalDRE")])[1]/text()').get(default="NAN")).replace('CalDRE #','')
            item['Agent_AreaServed']=Agent_AreaServed
            item['Agent_Designation'] = "NAN"
            item['Agent_Facebook']= response.xpath('//a[@aria-label="Follow me on Facebook"]/@href').get(default="NAN")
            item['Agent_Linkedin']=response.xpath('//a[@aria-label="Follow me on Linkedin"]/@href').get(default="NAN")
            item['Agent_Instagram']=response.xpath('//a[@aria-label="Follow me on Pinterest"]/@href').get(default="NAN")
            item['Agent_Twitter']=response.xpath('//a[@aria-label="Follow me on Twitter"]/@href').get(default="NAN")
            item['Agent_Pintrest'] = "NAN"
            item['Agent_Youtube']=response.xpath('//iframe[@title="youtube_small_iframe"]/@src').get(default="NAN")
            # item['Agent_Language']=Agent_Language
            item['Agent_Site'] = "NAN"
            item['Agent_Special_Tag']=Agent_Special_Tag
            item['Agent_Rating']=response.xpath('//span[@class="review-text font-fff pl-5 font-11 font-bold"]/span/text()').get(default="NAN")
            item['Office_Address']=(response.xpath('normalize-space((//*[@class="media__content"]/text()[2])[2])').get(default="NAN")+','+response.xpath('normalize-space((//*[@class="media__content"]/text()[3])[2])').get(default="NAN")).replace('"','')
            # item['Office_Address']=(response.xpath('normalize-space(//*[@id="ftcontainer"]/div[1]/div/div[2]/div[2]/text()[2])').get(default='null')+','+response.xpath('normalize-space(//*[@id="ftcontainer"]/div[1]/div/div[2]/div[2]/text()[3])').get(default='null')).replace('"','')
            item['Office_FAX'] = "NAN"
            item['Office_Branch']=response.xpath('//ul[@class="li-h li-h--breadcrumb li-h--inline"]/li[3]/a/span/text()').get(default="NAN")
            item['Office_Name']= response.xpath('//ul[@class="li-h li-h--breadcrumb li-h--inline"]/li[2]/a/span/text()').get(default="NAN")
            item['Office_Phone']=response.xpath('normalize-space(//div[@class="smallVPad"]/strong/a/text())').get(default="NAN")
            item['Office_Site'] = "NAN"
            item['Office_Zip'] = "["+ str(re.findall('\d{5}(?:[-\s]\d{4})?$',response.xpath('normalize-space((//*[@class="media__content"]/text()[3])[2])').get(default="NAN")))+"]"
            item['Company_Facebook']="https://www.facebook.com/BHGRealEstate"
            item['Company_Linkedin']="NAN"
            item['Company_Name'] = "Better Homes and Gardens Real Estate"
            item['Company_Site']="https://www.bhgre.com/"
            item['Company_Twitter'] = "http://twitter.com/BHGRealEstate"
            return item
            # //a[contains(text(),"Email")]
