from scrapy import Spider


class ColdwellBanker(Spider):

    name = 'coldwellbanker.com'
    allowed_domains = ['www.coldwellbanker.com']

    start_urls = ['https://www.coldwellbanker.com/real-estate-agents']

    def parse(self, response):
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

        office_phone = address.css('.f-icon-phone + strong::text').get()
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

        return {
            'Agent_URL': response.request.url,
            'Agent_Name': name,
            'Agent_DP': picture,
            'Agent_Tag': ' '.join(badges),
            'Agent_Phone': phone,
            'Agent_Rating': rating,
            'Agent_AreaServed': '|'.join(area_served),
            'Agent_License': agent_license,
            'Agent_Facebook': agent_fb,
            'Agent_Linkdin': agent_li,
            'Agent_Yelp': agent_yelp,
            'Agent_Instagram': agent_insta,
            'Agent_Twitter': agent_twitter,
            'Agent_Youtube': agent_youtube,
            'Office_Name': company,
            'Office_Branch': office_branch,
            'Office Phone': office_phone,
            'Office_Address': street + ' ' + city + ' ' + state,
            'Office_ZIP': ZIP,
            'Company_Facebook': company_facebook,
            'Company_Pinterest': company_pinterest,
            'Company_Twitter': company_twitter,
            'Company_Youtube': company_youtube

        }
