# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Century21Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    unique_id = scrapy.Field()
    agent_url = scrapy.Field()
    agent_dp = scrapy.Field()
    agent_name = scrapy.Field()
    agent_phone = scrapy.Field()
    agent_email = scrapy.Field()
    agent_role = scrapy.Field()
    agent_license = scrapy.Field()
    agent_areaserved = scrapy.Field()
    agent_designations = scrapy.Field()
    agent_facebook = scrapy.Field()
    agent_instagram = scrapy.Field()
    agent_twitter = scrapy.Field()
    agent_linkedin = scrapy.Field()
    agent_pinterest = scrapy.Field()
    agent_youtube = scrapy.Field()
    agent_site = scrapy.Field()
    agent_special_tag = scrapy.Field()
    agent_rating = scrapy.Field()
    office_address = scrapy.Field()
    office_fax = scrapy.Field()
    office_branch = scrapy.Field()
    office_name = scrapy.Field()
    office_phone = scrapy.Field()
    office_site = scrapy.Field()
    office_zip = scrapy.Field()
    office_state = scrapy.Field()
    other_phone = scrapy.Field()
    company_facebook = scrapy.Field()
    company_linkedin = scrapy.Field()
    company_name = scrapy.Field()
    company_site = scrapy.Field()
    company_twitter = scrapy.Field()
    date_of_data_extraction = scrapy.Field()
    data_extracted_by = scrapy.Field()
    dataextraction_uuid = scrapy.Field()

