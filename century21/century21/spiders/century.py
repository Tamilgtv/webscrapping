import scrapy
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
from ..items import Century21Item

class CenturySpider(scrapy.Spider):
    name = 'century'
    allowed_domains = ['www.century21.com']
    start_urls = ['https://www.century21.com/property-search-map']
    def __init__(self):
        self.agentdata_df = pd.DataFrame()
        self.unique_id = 0
    def parse(self, response):
        state_container = response.css('.stateInformationDiv')
        state_agent_urls = []
        for state_count in range(len(state_container)):
        # for state_count in range(0,1):
            sub_container = state_container[state_count].css('.stateLinkLabel')
            all_urls = [i.css('a::attr(href)').extract()[0] for i in sub_container]
            state_agent_url = ["https://www.century21.com"+i for i in all_urls if 'agents' in i][0]

            state_agent_urls.append(state_agent_url)
            yield scrapy.Request(url=state_agent_url,  callback=self.extract_urls,dont_filter = True)
        # yield state_agent_urls

    def extract_urls(self, response):
        result_count = response.css('.results-label *::text').extract()[-1]
        res = [str(i) for i in result_count if i.isdigit()]
        total_agents = int("".join(res))
        total_pages = int((total_agents/20)+1)
        #more_page_url = "https://www.century21.com"+response.css('.infinite-more-link::attr(href)').extract()[0]
        for data in response.xpath("//div[@class='agent-card-inner']"):
            award = data.xpath(".//div[@class='agent-president-award']/text()").get()
            awardnew=""
            if not award:
                award = awardnew
            else:
                awardnew = award.strip()
            for number in data.xpath(".//div[@class='agent-phone-info']"):
                phone=""
                mobile=""
                if number.xpath(".//div[@class='agent-phone'][2]"):
                    mobile = number.xpath(".//div[@class='agent-phone'][2]/a/text()").get()
                if number.xpath(".//div[@class='agent-phone']"):
                    if number.xpath(".//div[@class='agent-phone']/strong/text()")=="Mobile:":
                        mobile = number.xpath(".//div[@class='agent-phone']/a/text()").get()
                    else:
                        phone = number.xpath(".//div[@class='agent-phone']/a/text()").get()
                else:
                    phone = number.xpath(".//div[@class='office-phone']/a/text()").get()
            data_dict = {
                'OC_profile_pic_url' : data.xpath(".//div[@class='agent-card-image']//@style").re_first(r'url\((.*)\)'),
                'OC_name' : (data.xpath(".//div[@class='agent-card-primary-info']/a/text()").get()).strip(),
                'OC_profile_url': response.urljoin(data.xpath(".//div[@class='agent-card-primary-info']/a/@href").get()),
                'OC_award' : awardnew,
                'OC_phone' : phone,
                'OC_mobile' : mobile,
                'OC_branch' : (data.xpath(".//div[@class='agent-card-secondary-info']/a/text()").get()).strip()
            }

            data_df = pd.DataFrame(data_dict, index=[0], columns=['OC_profile_pic_url','OC_name','OC_profile_url','OC_award','OC_phone','OC_mobile','OC_branch'])
            self.agentdata_df = self.agentdata_df.append(data_df)
        try:
            more_page_url = "https://www.century21.com"+response.css('.infinite-more-link::attr(href)').extract()[0]
        except:
            try:
                more_page_url = "https://www.century21.com"+response.css("#pagination-next::attr(href)").extract()[0]
            except:
                more_page_url = ""

        print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
        print(more_page_url,"total_pages",total_pages)
        print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")

        if more_page_url !='':
            yield scrapy.Request(url=more_page_url, callback=self.extract_urls,dont_filter = True)
        if more_page_url == "":
            print(self.agentdata_df)
            for row in self.agentdata_df.iterrows():
                row = row[1]
                link = row['OC_profile_url']
                yield scrapy.Request(url=link,callback=self.parse_page)


    def parse_page(self, response):
        info_container = response.css("#BodyLeftLane")
        ###########################################################
        name = " ".join([tag.strip() for tag in info_container.css("#agentRightLane").css('h1 *::text').extract() if tag.strip()!='']).split(" of ")[0].strip()
        ###########################################################
        office_name = " ".join([tag.strip() for tag in info_container.css("#agentRightLane").css('h1 *::text').extract() if tag.strip()!='']).split(" of ")[-1].strip()

        address = " ".join([address.strip() for address in info_container.css(".addressBlock::text").extract() if address.strip()!=''])
        ###########################################################
        # phoneNumber = info_container.css(".phoneNumber::text").extract()[0]
        ###########################################################
        try:
            agentwebpage = info_container.css(".agentwebpage::attr(href)").extract()[0]
        except:
            agentwebpage = ""
        ###########################################################
            # ratingcount = info_container.css(".reviewCount *::text").extract()[0]
        ###########################################################
        try:
            rating = info_container.css(".overallRating").css('span *::text')[-1].get()
        except:
            rating = ""
        ###########################################################
        awards_str = ""
        designations_str = ""
        try:
            agent_info_tags = info_container.css("#agentLeftLane").css('.agentInfoList')
        except:
            agent_info_tags = []
        for info_tag in agent_info_tags:
            category = info_tag.css("h4::text").extract()[0].strip()
            if category == 'Awards':
                awards_str = "|".join(info_tag.css('li::text').extract())
            elif category == 'Professional Designations':
                designations_str = "|".join(info_tag.css('li::text').extract())
        ###########################################################
        try:
            areas_served_str = "|".join(info_container.css("#areaServed").css('li *::text').extract())
        except:
            areas_served_str = ""
        ###########################################################
        agent_profile_link = info_container.css("#agentPicContainer").css('img::attr(src)').get()
        ###########################################################
        soup = BeautifulSoup(response.text,'html.parser')
        info_container_soup = soup.find(id='BodyLeftLane')
        try:
            agent_mobile = info_container_soup.find(attrs={"data-ctc-track":'["agent-ADP-CTC","call-agent-mobile"]'}).text
        except:
            agent_mobile = ""
        try:
            team_mobile = info_container_soup.find(attrs={"data-ctc-track":'["team-ADP-CTC","call-team-mobile"]'}).text
        except:
            team_mobile = ""
        try:
            agent_phone = info_container_soup.find(attrs={"data-ctc-track":'["agent-ADP-CTC","call-agent-phone"]'}).text
        except:
            agent_phone = ""
        if agent_phone == '':
            agent_phone = agent_mobile
            agent_mobile = ""
        try:
            team_phone = info_container_soup.find(attrs={"data-ctc-track":'["team-ADP-CTC","call-team-phone"]'}).text
        except:
            team_phone = ""
        try:
            office_phone = info_container_soup.find(attrs={"data-ctc-track":'["office-ADP-CTC","call-office-phone"]'}).text
        except:
            office_phone = ""
        ###############
        other_phone_ = agent_mobile +'|'+team_mobile+"|"+team_phone
        other_phone_list = [phone.strip() for phone in other_phone_.split("|") if phone !='']
        other_phone = "|".join(other_phone_list)
        try:
            fax = info_container_soup.find(attrs={"itemprop":'faxNumber'}).text
        except:
            fax = ""
        try:
            language = info_container_soup.find(attrs={"itemprop":'availableLanguage'}).text
        except:
            language = ""
        ###########################################################
        ###########################################################
        self.unique_id += 1
        item = Century21Item()
        item['unique_id'] = "Century21_"+str(self.unique_id)
        item['agent_url'] = response.url
        item['agent_dp'] = agent_profile_link
        item['agent_name'] = name
        item['agent_phone'] = agent_phone
        item['agent_email'] = ""
        item['agent_role'] = 'Agent'
        item['agent_license'] = ""
        item['agent_areaserved'] = areas_served_str
        item['agent_designations'] = designations_str
        item['agent_facebook'] = ""
        item['agent_instagram'] = ""
        item['agent_twitter'] = ""
        item['agent_linkedin'] = ""
        item['agent_pinterest'] = ""
        item['agent_youtube'] = ""
        item['agent_site'] = agentwebpage
        item['agent_special_tag'] = ''
        item['agent_rating'] = rating
        item['office_address'] = address
        item['office_fax'] = fax
        item['office_branch'] = ''
        item['office_name'] = office_name
        item['office_phone'] = office_phone
        item['office_site'] = ''
        item['office_zip'] = address.strip().split(" ")[-1]
        item['office_state'] = address.strip().split(" ")[-2]
        item['other_phone'] = other_phone
        item['company_facebook'] = ''
        item['company_linkedin'] = ''
        item['company_name'] = 'century21'
        item['company_site'] = 'https://www.century21.com/'
        item['company_twitter'] = ''
        item['date_of_data_extraction'] = datetime.now()
        item['data_extracted_by'] = 'Pooja'
        item['dataextraction_uuid'] = 'Pooja-'+datetime.now().strftime('%m-%d-%Y')

        yield item
