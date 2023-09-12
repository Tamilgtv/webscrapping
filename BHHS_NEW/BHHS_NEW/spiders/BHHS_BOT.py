import scrapy
import re
class BhhsBotSpider(scrapy.Spider):
    name='BHHS_BOT'

         
    with open('D:/Tamil/AIMLEAP/CBN/CBN_BOT/BHHS_NEW/bhhs_link_1.csv') as f:
         start_urls = [line.strip() for line in f]

    def parse(self, response):
        # languages= list(filter(None, [
        #             text.get().replace('\n', '').strip("<li>").strip("</")
        #             for text in
        #             response.xpath('//*[@id="languages"]/li')
        #         ]))[0:6]

        fax=response.xpath("(//div[@class='cmp-agent-details details row']/ul/li/em/text())[3]").get(default = "-")
        number = response.xpath("(//div[@class='cmp-agent-details details row']/ul/li/em/text())[2]").get(default = "-")
        offnum = response.css("li:nth-child(1) .cmp-agent-details__phone-number::text").get(default = "-")
        Agent_no = response.xpath("//div[@class='cmp-agent-details details row']/ul/li/a/text()").get(default ="-")
        Agent_dp = [response.xpath("//meta[@property='og:image']/@content").get(default ="-")]
        name = [response.css(".homepage_link::text").get(default ="-")]
        # address = list(filter(None, [
        #             text.get().replace('\n', '').strip("")
        #             for text in
        #             response.css('.cmp-agent__office::text')
        #         ]))[0:6]
        address = (str(response.css('.cmp-agent__office::text').get()).strip()).split("\n")
        print(address)
        print("????????????????????????????"+str(len(address))+"-----????????????////////////////////")
        special_tag = [response.css("#accreditations li::text").get(default ="-")]
        agent_license = [response.xpath("//ul[@class='cmp-agent-details__license text-uppercase d-flex flex-column flex-lg-row flex-wrap']/@data-license").get(default ="-")]
        agent_site = [response.css(".cmp-agent-details__website::text").get(default ="-")]
        about = [response.css("#biotxt::text").get(default ="-")]
        email = [response.xpath("//*[@class='cmp-agent-details__mail text-lowercase']/@href").get(default ="-")]
        role = [response.css(".cmp-agent__title::text").get(default ="-")]
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
        yield{
            'Agent_URL': [response.url],
            'Agent_DP': Agent_dp,
            'Agent_Name': name,
            'Agent_Phone':num,
            'Phone_type':P_type,
            'Agent_Email':str(email).replace('mailto:','').replace('[','').replace(']',''),
            'Agent_Role':role,
            'Agent_License':agent_license,
            'Agent_AreaServed': '-',
            'Agent_Designation': role,
            'Agent_bio': about,
            # 'Agent_Language':languages,
            'Agent_Facebook':fb,
            'Agent_Linkedin':lin,
            'Agent_Instagram':insta,
            'Agent_Twitter':tw,
            'Agent_Pinterest':"-",
            'Agent_Youtube':yout,
            'Agent_Site':agent_site,
            'Agent_Special_Tag':special_tag,
            'Agent_Rating':"-",
            'Office_Address':(str(address[2])+","+str(address[3]).strip()).strip(),
            'Office_Fax':faxno,
            'Office_Branch':(str(address[0])+","+str(address[1].strip())).strip(),
            'Office_Phone':offnum,
            'office_site':"-",
            'office_Zip':str(re.findall('\d{5}(?:[-\s]\d{4})?$',str(address[-1]).strip())),
            'Other_phone':'-',
            'Company_Facebook':"-",
            'Company_Linkedin':"-",
            'Company_Name':"Berkshire Hathaway HomeServices",
            'Company_site':"https://www.bhhs.com/",
            'Company_Twitter':"-",



        }
