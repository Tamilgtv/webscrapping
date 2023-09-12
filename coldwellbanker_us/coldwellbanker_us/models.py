from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL
from sqlalchemy import Integer, ForeignKey, String, Column, TIMESTAMP, BIGINT, Boolean, VARCHAR, NUMERIC,JSON
from . import settings


DeclarativeBase = declarative_base()


def db_connect():
    """ Performs database connections using database settings from settings.py
        Returns sqlalchemy engine instance
    """
    engine = create_engine(settings.postgres_connection_url, echo=True)
    return engine
    # return create_engine(URL(**settings.DATABASE))


def create_table(engine):
    """"""
    DeclarativeBase.metadata.create_all(engine)

class Data_Table(DeclarativeBase):
    """
    Defines the items model
    """
    __tablename__ = "internal_data_exctraction"
    
    unique_id =  Column("unique_id",String, primary_key=True, nullable=False)
    agent_url = Column("agent_url",String, nullable=True)
    agent_dp = Column("agent_dp",String, nullable=True)
    agent_name = Column("agent_name",String, nullable=False)
    agent_phone = Column("agent_phone",String, nullable=True)
    agent_email = Column("agent_email",String, nullable=True)
    agent_role = Column("agent_role",String, nullable=True)
    agent_license = Column("agent_license",String, nullable=True)
    agent_areaserved = Column("agent_areaserved",String, nullable=True)
    agent_designations = Column("agent_designations",String, nullable=True)
    agent_facebook = Column("agent_facebook",String, nullable=True)
    agent_instagram = Column("agent_instagram",String, nullable=True)
    agent_twitter = Column("agent_twitter",String, nullable=True)
    agent_linkedin =Column("agent_linkedin",String, nullable=True)
    agent_pinterest = Column("agent_pinterest",String, nullable=True)
    agent_youtube = Column("agent_youtube",String, nullable=True)
    agent_site = Column("agent_site",String, nullable=True)
    agent_special_tag = Column("agent_special_tag",String, nullable=True)
    agent_rating = Column("agent_rating",String, nullable=True)
    office_address = Column("office_address",String, nullable=True)
    office_fax = Column("office_fax",String, nullable=True)
    office_branch = Column("office_branch",String, nullable=True)
    office_name = Column("office_name",String, nullable=True)
    office_phone = Column("office_phone",String, nullable=True)
    office_site = Column("office_site",String, nullable=True)
    office_zip = Column("office_zip",String, nullable=True)
    office_state = Column("office_state",String, nullable=True)
    other_phone = Column("other_phone",String, nullable=True)
    company_facebook = Column("company_facebook",String, nullable=True)
    company_linkedin = Column("company_linkedin",String, nullable=True)
    company_name = Column("company_name",String, nullable=True)
    company_site = Column("company_site",String, nullable=True)
    company_twitter = Column("company_twitter",String, nullable=True)
    date_of_data_extraction = Column("date_of_data_extraction",TIMESTAMP(timezone=True))
    data_extracted_by = Column("data_extracted_by",String, nullable=True)
    dataextraction_uuid = Column("dataextraction_uuid",String, nullable=True)




    def __init__(self, unique_id , agent_url, agent_dp,agent_name,agent_phone,agent_email,agent_role,agent_license,agent_areaserved,
                 agent_designations,agent_facebook,agent_instagram,agent_twitter,agent_linkedin,agent_pinterest,
                 agent_youtube,agent_site,agent_special_tag,agent_rating,office_address,office_fax,office_branch,office_name,
                 office_phone,office_site,office_zip,office_state,other_phone,company_facebook,company_linkedin,company_name,
                 company_site,company_twitter,date_of_data_extraction,data_extracted_by,dataextraction_uuid):
        self.unique_id = unique_id
        self.agent_url = agent_url
        self.agent_dp = agent_dp
        self.agent_name = agent_name
        self.agent_phone = agent_phone
        self.agent_email = agent_email
        self.agent_role = agent_role
        self.agent_license =  agent_license
        self.agent_areaserved =  agent_areaserved
        self.agent_designations =  agent_designations
        self.agent_facebook = agent_facebook
        self.agent_instagram = agent_instagram
        self.agent_twitter = agent_twitter
        self.agent_linkedin = agent_linkedin
        self.agent_pinterest = agent_pinterest
        self.agent_youtube = agent_youtube
        self.agent_site = agent_site
        self.agent_special_tag = agent_special_tag
        self.agent_rating = agent_rating
        self.office_address = office_address
        self.office_fax = office_fax
        self.office_branch = office_branch
        self.office_name = office_name
        self.office_phone = office_phone
        self.office_site = office_site
        self.office_zip = office_zip
        self.office_state = office_state
        self.other_phone = other_phone
        self.company_facebook = company_facebook
        self.company_linkedin = company_linkedin
        self.company_name = company_name
        self.company_site = company_site
        self.company_twitter = company_twitter
        self.date_of_data_extraction = date_of_data_extraction
        self.data_extracted_by = data_extracted_by
        self.dataextraction_uuid = dataextraction_uuid
    
