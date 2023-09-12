import scrapy
from coldwellbanker_us import items
from datetime import datetime

class ColdwellbankerSpider(scrapy.Spider):
    name = 'coldwellbanker'
    allowed_domains = ['coldwellbanker.com']
    start_urls = ['https://www.coldwellbanker.com/real-estate-agents']

    def parse(self, response):
        self.count = 0
        yield from response.follow_all(
            css='.areaListCol > span > a',   # State-wise brokerage lists
            callback=self.parse_state
        )

    def parse_state(self, response):
        yield from response.follow_all(
            css='.l-grid.pb-20 > ul > li:first-child > a',   # Brokeage pages
            callback=self.parse_brokerage
        )

    def parse_brokerage(self, response):
        yield from response.follow_all(
            css='.pod__office > h3 > a',   # Office pages, near the bottom
            callback=self.parse_office
        )

    def parse_office(self, response):
        yield from response.follow_all(
            css='.results-row > a',
            callback=self.parse_agent
        )

    def parse_agent(self, response):
        item = items.ColdwellbankerUsItem()

        self.count = self.count + 1
        name = response.css('.agent-heading h1[itemprop=name]::text').get()
        phone = response.css('.agent-info-cont__agent-phone > a::text').get()
        badges = response.css(
            '.agent-info-cont__agent-icons img::attr(alt)'
        ).getall()

        address = response.css('.broker-ftr .f-left .media .media__content')
        company = address.css('.mls-company-name::text').get()

        addrlines = address.xpath('text()[normalize-space()]').getall()
        street = addrlines[0].strip()
        city, state_ZIP = addrlines[1].strip().split(',', maxsplit=1)
        state, ZIP = state_ZIP.strip().split(' ', maxsplit=1)

        office_phone = response.xpath('//*[@class = "smallVPad"]/strong/a/text()').get()
        if office_phone:
            office_phone = office_phone.strip()

        rating = response.css(
            '#star-ratings > .review-text > span::text'
        ).get()

        area_served = response.css('#all-areas-list li a::text').getall()

        agent_license = response.css('.agent-heading span::text').get()

        agent_fb = response.css('.fm-fb::attr(href)').get()
        agent_li = response.css('fm-li::attr(href)').get()
        agent_yelp = response.css('fm-y::attr(href)').get()
        agent_insta = response.css('fm-ig::attr(href)').get()
        agent_twitter = response.css('fm-t::attr(href)').get()

        agent_youtube = response.css(
                '[title~=youtube_small_iframe]::attr(src)').get()

        company_social_links = response.css(
            '.social-network-links-container ul li a::attr(href)').getall()
        company_facebook = company_social_links[0]
        company_pinterest = company_social_links[1]
        company_twitter = company_social_links[2]
        company_youtube = company_social_links[3]

        off_branch = response.css(
            '.li-h li a span[itemprop=title]::text').getall()
        office_branch = off_branch[2]

        picture = response.css('.media img[itemprop=image]::attr(src)').get()

        # return {
        #     'Agent_URL': response.request.url,
        #     'Agent_Name': name,
        #     'Agent_DP': picture,
        #     'Agent_Tag': ' '.join(badges),
        #     'Agent_Phone': phone,
        #     'Agent_Rating': rating,
        #     'Agent_AreaServed': '|'.join(area_served),
        #     'Agent_License': agent_license,
        #     'Agent_Facebook': agent_fb,
        #     'Agent_Linkdin': agent_li,
        #     'Agent_Yelp': agent_yelp,
        #     'Agent_Instagram': agent_insta,
        #     'Agent_Twitter': agent_twitter,
        #     'Agent_Youtube': agent_youtube,
        #     'Office_Name': company,
        #     'Office_Branch': office_branch,
        #     'Office Phone': office_phone,
        #     'Office_Address': street + ' ' + city + ' ' + state,
        #     'Office_ZIP': ZIP,
        #     'Company_Facebook': company_facebook,
        #     'Company_Pinterest': company_pinterest,
        #     'Company_Twitter': company_twitter,
        #     'Company_Youtube': company_youtube
        #     }
        
            
        item['unique_id'] = 'Coldwellbanker_'+str(self.count)
        item['agent_url'] = response.request.url
        item['agent_dp'] = picture
        item['agent_name'] = name
        item['agent_phone'] = phone.replace('Mobile:','').replace('Direct:','').replace('-','').replace('(','').replace(')','').replace(' ','')
        item['agent_email'] = ''
        item['agent_role'] = 'Agent'
        item['agent_license'] = agent_license
        item['agent_areaserved'] = '|'.join(area_served)
        item['agent_designations'] = ''
        item['agent_facebook'] = agent_fb
        item['agent_instagram'] = agent_insta
        item['agent_twitter'] = agent_twitter
        item['agent_linkedin'] = agent_li
        item['agent_pinterest'] = ''
        item['agent_youtube'] = agent_youtube
        item['agent_site'] = ''
        item['agent_special_tag'] = ' '.join(badges)
        item['agent_rating'] = rating
        item['office_address'] = street + ' ' + city + ' ' + state
        item['office_fax'] = ''
        item['office_branch'] = office_branch
        item['office_name'] = company
        item['office_phone'] = office_phone
        item['office_site'] = ''
        item['office_zip'] = ZIP
        item['office_state'] = state
        item['other_phone'] = ''
        item['company_facebook'] = company_facebook
        item['company_linkedin'] = ''
        item['company_name'] = 'Coldwellbanker'
        item['company_site'] = 'https://www.coldwellbanker.com'
        item['company_twitter'] = company_twitter
        item['date_of_data_extraction'] = datetime.now()
        item['data_extracted_by'] = 'Tamil'
        item['dataextraction_uuid'] = 'Tamil-'+datetime.now().strftime('%m-%d-%Y')

        yield item
            
            
            
            
            
            
            

    
    
    
    
    
