import scrapy
import re
class RealbotSpider(scrapy.Spider):
    name = 'realbot'
    allowed_domains = ['www.realtyexecutives.com']
    # start_urls = ['https://www.realtyexecutives.com/offices/us/'+str(line.strip() for line in state_list) ]
    def start_requests(self):
        state_list =['ca','al','ak','az']
        for i in state_list[:1]:
            yield scrapy.Request(url='https://www.realtyexecutives.com/offices/us/'+str(i), callback=self.parse,headers= {
                'user_agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
            })
            
    def parse(self, response):
        office = response.xpath('//a[@class="office-search-2"]/@href')
        yield from response.follow_all(office, callback=self.agent_links)
        next = ("(//span/a[contains(text(),'next')])[1]/@href")
        yield from response.follow_all(next, callback=self.parse)
    def agent_links(self,response):
        agents = response.xpath('//div[@class="card-content"]/div/a/@href')
        yield from response.follow_all(agents, callback=self.agent_details)
        next = ("(//span/a[contains(text(),'next')])[1]/@href")
        yield from response.follow_all(next, callback=self.agent_links)
    def agent_details(self,response):
        # getting Agent dp link
        Agent_DP = response.xpath('normalize-space(//div[@class="profile-img"]/div/@style)').get(default="NAN")
        Agent_Name = response.xpath('//div[@class="about-entity"]/h1/span/text()').get(default="NAN")
        Agent_Mob = response.xpath('normalize-space(//a[@id="agentDetailsPhone"]/span/text())').get(default="Not Found")
        ph =  str("|".join([txt.strip() for txt in response.xpath('//span[@itemprop="telephone"]/parent::p').getall()]))
        other_Phone = ph.replace("<p>","").replace(' <span itemprop="telephone">',"").replace("</span></p>","")
        otr_ph = other_Phone.split("|")
############# Mobile Number################################
        if Agent_Mob != "Not Found":
            Agent_Mobile =re.sub('[\W_]+', '', Agent_Mob)
        else:
            Agent_Mobile =re.sub('[\W_]+', '', str(otr_ph[0]))
#################### cleaning mobile number##########################

        try:
            if Agent_Mobile[0]=='1':
                mobile =Agent_Mobile[1:11]
            elif len(Agent_Mobile)>10:
                mobile =Agent_Mobile[0:10]
            elif len(Agent_Mobile) == 0:
                mobile ='Not Found'
            else:
                mobile = Agent_Mobile
        except IndexError:
            mobile = "Not Found"

#######################Phone Type#######################
        if Agent_Mob !='Not Found':
            Phone_Type = "Phone"
        else:
            Phone_Type = "NAN"
        ph =  str("|".join([txt.strip() for txt in response.xpath('//span[@itemprop="telephone"]/parent::p').getall()]))
        other_Phone = ph.replace("<p>","").replace(' <span itemprop="telephone">',"").replace("</span></p>","")
        # getting Agent licence
        Dre = response.xpath('normalize-space(//p[contains(text(),"DRE:")])').get(default="NAN")
        # getting Agent facebook
        Agent_Facebook = response.xpath('//a[contains(@href,"https://www.facebook.com/")]/@href').get(default="NAN")
        # getting Agent  twitter
        Agent_twitter = response.xpath('//a[contains(@href,"https://twitter.com/")]/@href').get(default="NAN")
        # getting Agent  linkedin
        Agent_Linkedin = response.xpath('//a[contains(@href,"https://www.linkedin.com/")]/@href').get(default="NAN")
        # getting Agent youtube
        Agent_youtube = response.xpath('//a[contains(@href,"https://www.youtube.com/")]/@href').get(default="NAN")
        # getting Agent instagrem
        Agent_insta = response.xpath('//a[contains(@href,"https://www.instagram.com/")]/@href').get(default="NAN")
        # getting Agent pinterest
        Agent_pinterest = response.xpath('//a[contains(@href,"https://www.pinterest.com/")]/@href').get(default="NAN")
        # getting office address
        Office_Address= response.xpath('normalize-space((//div[@itemprop="address"])[2])').extract_first(default="NAN")
        # getting office zip
        office_zip= response.xpath('normalize-space((//div[@itemprop="address"])[2]/p[2]/span[3]/text())').get(default="NAN")
        # getting office site
        office_web = response.xpath('(//a[@class="dk-blue-button"])[2]/@href').get(default="NAN")
        # getting office name
        Office_name = response.xpath('//div[@class="col-sm-5"]/div[4]/text()').get(default="NAN")
        #agent special tag
        about = response.xpath('normalize-space((//div[@class="row"])[3])').extract_first(default="NAN")

        # getting agent details

        yield{
            'Agent_URL':response.request.url,
            'Agent_Dp':Agent_DP.replace("background-image: url('","").replace("')'",""),
            'Agent_Name':Agent_Name,
            'Agent_Phone':mobile,
            "Phone_Type":Phone_Type,
            'Other_Phone':other_Phone,
            "Phone_Type2":'Other_Phone',
            'Agent_Email':'NAN',
            'Agent_Role':"Broker",
            'Agent_Licence':Dre,
            'Agent_AreaServed':'NAN',
            'Agent_Designation':'NAN',
            'Agent_Facebook':Agent_Facebook,
            'Agent_Linkedin':Agent_Linkedin,
            'Agent_instagram': Agent_insta,
            'Agent_Twitter':Agent_twitter,
            'Agent_pinterest_': Agent_pinterest,
            'Agent_Youtube':Agent_youtube,
            'Agent_Site':'NAN',
            'Agent_Special_Tag':about,
            'Agent_Rating':'NAN',
            'Office_Address':Office_Address,
            'Office_Fax':'NAN',
            'Office_Branch':'NAN',
            'Office_Name':Office_name,
            'Office_Site':office_web,
            'Office_zip':office_zip,
            'Company_Facebook':'https://www.facebook.com/realtyexecutivesintl',
            'Company_Linkedin':'http://www.linkedin.com/company/realty-executives',
            'Company_Name':'Realty Executives',
            'Company_Site':'https://www.realtyexecutives.com/',
            'Company_Twitter':'https://twitter.com/realtyexec'



        }
