import scrapy
from coldwellbanker_ca import items
from datetime import datetime

class ColdwellbankerSpider(scrapy.Spider):
    name = 'coldwellbanker'
    allowed_domains = ['coldwellbanker.ca']
    #start_urls = ['https://www.coldwellbanker.ca/agents/ca']
    #with open('D:/Tamil/AIMLEAP/CBN/CBN_BOT/coldwellbanker_ca/All_agent_ca.csv') as f:
    with open('All_agent_ca.csv') as f:
         start_urls = [line.strip() for line in f][1:]
         #start_urls = agent_ca_link[1:]
    # custom_settings = {
    #     'DOWNLOAD_DELAY': 10,
    #     'CONCURRENT_REQUESTS_PER_DOMAIN': 1
    # }

    # def parse(self, response):
    #     self.count = 0
    #     yield from response.follow_all(
    #         css='.agent-view-listing > a',
    #         callback=self.parse_profile
    #     )

    #     next = response.css('.pagination > .next-page > a')
    #     if next:
    #         yield response.follow(
    #             url=next[0],
    #             callback=self.parse
    #         )

    #def parse_profile(self, response):
    def parse(self, response):
        self.count = self.count + 1
        item = items.ColdwellbankerCaItem()
        name = response.css('.agent-name::text').get()
        position = response.css('.job-title::text').get()
        badges = response.css(
            'agent-badge agent-badge-image::attr(alt)'
        ).getall()

        mobile = response.xpath(
            '//address[@class="agent-contacts"]'
            '/p[contains(text(), "Mobile:")]/span/text()'
        ).get()

        off_phone = response.xpath(
            '//address[@class="agent-contacts"]'
            '/p[contains(text(), "Office:")]/span/text()'
        ).get()

        fax = response.xpath(
            '//address[@class="agent-contacts"]'
            '/p[contains(text(), "Fax:")]/span/text()'
        ).get()

        web = response.xpath(
            '//address[@class="agent-contacts"]'
            '/p[contains(text(), "Web:")]/a/@href'
        ).get()

        email = response.xpath(
            '//div[@class="agent-contacts-actions"]'
            '//a[contains(i/@class, "fa-envelope-o")]/@href'
        ).get()
        if email:
            email = email.partition(':')[2]

        facebook = response.xpath(
            '//div[@class="agent-contacts-actions"]'
            '/a[contains(i/@class, "fa-facebook")]/@href'
        ).get()
        linkdin = response.xpath(
            '//div[@class="agent-contacts-actions"]'
            '//a[contains(i/@class, "fa-linkedin")]/@href'
        ).get()
        twitter = response.xpath(
            '//div[@class="agent-contacts-actions"]'
            '//a[contains(i/@class, "fa-twitter")]/@href'
        ).get()

        office = response.css('address.agent-office > a > span::text').get()
        street, address = response.css(
            'address.agent-office > span > span::text'
        ).getall()
        region, ZIP = address.rsplit(' ', maxsplit=1)
        city, state = region.split(',')

        picture = response.css('.profile-image img::attr(src)').get()

        # return {
        #     'Agent_URL': response.request.url,
        #     'Agent_Name': name,
        #     'Agent_picture': picture,
        #     'Agent_Role': position,
        #     'Agent_Tag': '; '.join(badges),
        #     'Agent_Phone': mobile,
        #     'Office_Phone': off_phone,
        #     'Agent_Fax': fax,
        #     'Agent_Web': web,
        #     'Agent_Facebook': facebook,
        #     'Agent_Linkdin': linkdin,
        #     'Agent_Twitter': twitter,
        #     'Office_Name': office,
        #     'Office_Address': street + ' ' + city + ' ' + state,
        #     'Office_Street': street,
        #     'Office_City': city,
        #     'Office_State': state,
        #     'Office_ZIP': ZIP
        # }

        item['unique_id'] = 'Coldwellbanker_ca_'+str(self.count)
        item['agent_url'] = response.request.url
        item['agent_dp'] = picture
        item['agent_name'] = name
        item['agent_phone'] = mobile.replace('Mobile:','').replace('Direct:','').replace('-','').replace('(','').replace(')','').replace(' ','')
        item['agent_email'] = ''
        item['agent_role'] = position
        item['agent_license'] = ''
        item['agent_areaserved'] = ''
        item['agent_designations'] = ''
        item['agent_facebook'] = facebook
        item['agent_instagram'] = ''
        item['agent_twitter'] = twitter
        item['agent_linkedin'] = linkdin
        item['agent_pinterest'] = ''
        item['agent_youtube'] = ''
        item['agent_site'] = web
        item['agent_special_tag'] = '; '.join(badges)
        item['agent_rating'] = ''
        item['office_address'] = street + ' ' + city + ' ' + state
        item['office_fax'] = fax
        item['office_branch'] = ''
        item['office_name'] = office
        item['office_phone'] = off_phone
        item['office_site'] = ''
        item['office_zip'] = ZIP
        item['office_state'] = state
        item['other_phone'] = ''
        item['company_facebook'] = ''
        item['company_linkedin'] = ''
        item['company_name'] = 'Coldwellbanker'
        item['company_site'] = 'https://www.coldwellbanker.ca'
        item['company_twitter'] = ''
        item['date_of_data_extraction'] = datetime.now()
        item['data_extracted_by'] = 'Tamil'
        item['dataextraction_uuid'] = 'Tamil-'+datetime.now().strftime('%m-%d-%Y')

        yield item       







