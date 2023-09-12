# -*- coding: utf-8 -*-
import scrapy


class ColdwellbankercaSpider(scrapy.Spider):
    name = 'coldwellbankerca'
    allowed_domains = ['coldwellbanker.ca']
    #start_urls = ['http://coldwellbanker.ca/']

    start_urls = ['https://www.coldwellbanker.ca/agents/ca']
    custom_settings = {
        'DOWNLOAD_DELAY': 10,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1
    }

    def parse(self, response):
        yield from response.follow_all(
            css='.agent-view-listing > a',
            callback=self.parse_profile
        )

        next = response.css('.pagination > .next-page > a')
        if next:
            yield response.follow(
                url=next[0],
                callback=self.parse
            )

    def parse_profile(self, response):
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

        return {
            'Agent_URL': response.request.url,
            'Agent_Name': name,
            'Agent_picture': picture,
            'Agent_Role': position,
            'Agent_Tag': '; '.join(badges),
            'Agent_Phone': mobile,
            'Office_Phone': off_phone,
            'Agent_Fax': fax,
            'Agent_Web': web,
            'Agent_Facebook': facebook,
            'Agent_Linkdin': linkdin,
            'Agent_Twitter': twitter,
            'Office_Name': office,
            'Office_Address': street + ' ' + city + ' ' + state,
            'Office_Street': street,
            'Office_City': city,
            'Office_State': state,
            'Office_ZIP': ZIP
        }
