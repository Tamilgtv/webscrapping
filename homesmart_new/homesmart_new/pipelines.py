# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from sqlalchemy.orm import sessionmaker
from . models import db_connect, create_homesmart_table, homesmart

class HomesmartNewPipeline(object):
    def __init__(self):
        """ Initialize database connection and sessionmaker """
        engine = db_connect()
        create_homesmart_table(engine)
        self.Session = sessionmaker(bind=engine)
    def process_item(self, item, spider):
        if isinstance(item, dict):
            pass
        else:
            session = self.Session()
            if item.get('company_name') == "HOMESMART":
                data = homesmart(item.get('agent_url'),item.get('agent_dp'),item.get('agent_name'),
                                 item.get('agent_phone'),item.get('agent_email'),item.get('agent_role'),item.get('agent_license'),
                                 item.get('agent_areaserved'),item.get('agent_designation'),item.get('agent_facebook'),item.get('agent_instagram'),
                                 item.get('agent_twitter'),item.get('agent_linkedin'),item.get('agent_pinterest'),item.get('agent_youtube'),
                                 item.get('agent_site'),item.get('agent_special_tag'),item.get('agent_rating'),item.get('office_address'),
                                 item.get('office_fax'),item.get('office_branch'),item.get('office_name'),item.get('office_phone'),
                                 item.get('office_site'),item.get('office_zip'),item.get('office_state'),item.get('other_phone'),
                                 item.get('company_facebook'),item.get('company_linkedin'),item.get('company_name'),item.get('company_site'),
                                 item.get('company_twitter'),item.get('date_of_data_extraction'),item.get('data_extracted_by'),item.get('dataextraction_uuid'),
                                 item.get('datacleaned_uuid'),item.get('uploading'))
    
            
            
            try:
                session.add(data)
                session.commit()
            except:
                session.rollback()
                raise
            finally:
                session.close()