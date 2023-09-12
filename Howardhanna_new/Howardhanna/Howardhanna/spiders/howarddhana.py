import scrapy
from ..items import HowardhannaItem
from datetime import datetime 

class HowardSpider(scrapy.Spider):
    name = 'howardhanna'
    page_no = 1
    start_urls = ['https://www.howardhanna.com/Agent/List?OrderBy=NameDesc&PageSize=100&Page=1']
    base_url = "https://www.howardhanna.com"



########### Here we are collecting all the Agent Links  #####################
    def __init__(self):
        
        self.unique_id = 0
        
    def parse(self, response):
        
        for link in response.xpath("//*[@id='A-Z']/div/div/div/div/a/@href"):
            all_links = self.base_url + link.get()

            yield scrapy.Request(all_links, callback=self.parse_profile)


        next_page = "https://www.howardhanna.com/Agent/List?OrderBy=NameDesc&PageSize=100&Page=" + str(HowardSpider.page_no)
        if HowardSpider.page_no < 102:
            HowardSpider.page_no += 1
            yield response.follow(next_page, callback = self.parse)


########## Here we are parsing every Agent Link to collect the Information  ##################


    def parse_profile(self, response):
######## Extracting Agent Name
        try:
            name = response.xpath("normalize-space(/html[1]/body[1]/div[1]/div[5]/div[1]/div[1]/div[1]/h1[1]/text())").get()
        except:
            name = ''

######## Extracting Agent Role
        try:
            role = response.xpath("normalize-space(//*[@class='display-block']/text())").get()
        except:
            role = ''

######## Extracting Agent DP
        try:
            image = response.xpath("//*[@class='entityPhotoRadius center-block']/img/@src")
            agent_dp = self.base_url + image.get()
        except:
            image = response.xpath("//*[@class='entityPhotoRadius']/img/@src")
            agent_dp = self.base_url + image.get()

######## Counting Total Number of <br> tags in address
        get_no = response.xpath("//*[@class='font-13 p-b-5']//br/following-sibling::text()")
        counted_no = len(get_no) - 1
        if len(get_no) == 5:
            first, second, third = 1, 2, 3
        elif len(get_no) == 4:
            first, second, third = 1, 2, 0
        else:
            first, second, third = 0, 0, 0

######## Extracting Office Address
        try:
            address = response.xpath("normalize-space(//*[@class='font-13 p-b-5']/strong/a/text())").get()
        except:
            address = ''
        try:
            street = response.xpath(
                "normalize-space((//*[@class='font-13 p-b-5']//br/following-sibling::text())[" + str(
                    first) + "])").get()
        except:
            street = ''
        try:
            street2 = response.xpath(
                "normalize-space((//*[@class='font-13 p-b-5']//br/following-sibling::text())[" + str(
                    second) + "])").get()
        except:
            street2 = ''
        try:
            location = response.xpath(
                "normalize-space((//*[@class='font-13 p-b-5']//br/following-sibling::text())[" + str(
                    third) + "])").get()
        except:
            location = ''
        try:
            if len(get_no) == 5:
                complete_address = address + ', ' + street + ', ' + street2 + ', ' + location
            elif len(get_no) == 4:
                complete_address = address + ', ' + street + ', ' + street2
            else:
                complete_address = ''
        except:
            complete_address = ''

######## Extracting Office Zip
        try:
            if len(get_no) == 5:
                office_zip = location[-5:]
            elif len(get_no) == 4:
                office_zip = street2[-5:]
            else:
                office_zip = ''
        except:
            office_zip = ''

######## Extracting Office Number
        try:
            office_no = response.xpath("normalize-space((//*[@class='font-13 p-b-5']//br/following-sibling::text())["+str(counted_no)+"])").get()
        except:
            office_no = ''
######## Extracting Agent Facebook
        try:
            facebook = response.xpath("//*[@class='icon-facebook-square text-facebook ']/@href").get()
        except:
            facebook = ''
######## Extracting Agent Twitter
        try:
            twitter = response.xpath("//*[@class='icon-twitter-square text-twitter ']/@href").get()
        except:
            twitter = ''
######## Extracting Agent Instagram
        try:
            instagram = response.xpath("//*[@class='icon-instagram-square text-instagram ']/@href").get()
        except:
            instagram = ''
######## Extracting Agent Youtube
        try:
            youtube = response.xpath("//*[@class='icon-youtube-square text-youtube ']/@href").get()
        except:
            youtube = ''
######## Extracting Agent Linkedin
        try:
            linkedln = response.xpath("//*[@class='icon-linkedin-square text-linkedin ']/@href").get()
        except:
            linkedln = ''
######## Extracting Agent Mobile
        try:
            mobile = response.xpath("//td[@class='vAlignMiddle p-t-3']/i[contains(@title,'Mobile Phone')]/../../td[contains(@class,'vAlignMiddle p-t-5 p-l-10 font-14 font-md-16 text-black')]/a/text()").get(default='')
            if mobile == '':
                mobile = response.xpath("//*[@title='Mobile Phone']/../../td[@class='vAlignMiddle p-l-10 font-13']/text()").get(default = '')
        except:
            mobile = response.xpath("//*[@title='Mobile Phone']/../../td[@class='vAlignMiddle p-l-10 font-13']/text()").get()
######## Extracting Agent alternate number
        try:
            alternate_no = response.xpath("//td[@class='vAlignMiddle p-t-3']/i[contains(@title,'Voicemail')]/../../td[contains(@class,'vAlignMiddle p-t-5 p-l-10 font-14 font-md-16 text-black')]/a/text()").get()
        except:
            alternate_no = response.xpath("//*[@title='Phone']/../../td[@class='vAlignMiddle p-l-10 font-13']/text()").get()
######## Extracting Office Fax
        try:
            fax = response.xpath("//td[@class='vAlignMiddle p-t-3']/i[contains(@title,'Fax')]/../../td[contains(@class,'vAlignMiddle p-t-5 p-l-10 font-14 font-md-16 text-black')]/a/text()").get()
        except:
            fax = response.xpath("//*[@title='Fax']/../../td[@class='vAlignMiddle p-l-10 font-13']/text()").get()
######## Extracting Agent Website
        try:
            agent_website = response.xpath("//td[@class='vAlignMiddle p-t-3']/i[contains(@title,'Website')]/../../td[contains(@class,'vAlignMiddle p-t-5 p-l-10 font-14 font-md-16 text-black')]/a/@href").get()
        except:
            agent_website = ''

        # yield{
        #     'Agent_URL': response.url,
        #     'Agent_DP': agent_dp,
        #     'Agent_Name': name,
        #     'Agent_Phone': mobile,
        #     'Alternate_no':alternate_no,
        #     'Agent_Role': role,
        #     'Agent_Facebook': facebook,
        #     'Agent_Linkedin': linkedln,
        #     'Agent_Instagram': instagram,
        #     'Agent_Twitter': twitter,
        #     'Agent_Youtube': youtube,
        #     'Agent_Site': agent_website,
        #     'Office_Address': complete_address,
        #     'Office_number':office_no,
        #     'Office_Fax': fax,
        #     'Office_Zip':office_zip
        # }
        try:
            state = complete_address.strip().split(' ')[-2]
        except:
            state = ''


        self.unique_id += 1

        item = HowardhannaItem()
        item['unique_id'] = "howardhanna_"+str(self.unique_id)
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
        item['company_name'] = 'Howardhanna'
        item['company_site'] = 'https://www.howardhanna.com'
        item['company_twitter'] = ''
        item['date_of_data_extraction'] = datetime.now()
        item['data_extracted_by'] = 'Tamil'
        item['dataextraction_uuid'] = 'Tamil-'+datetime.now().strftime('%m-%d-%Y')

        yield item





### Get the output in csv file using: scrapy crawl howardhanna.csv -O (filename).csv