import scrapy
from bs4 import BeautifulSoup
from datetime import datetime
from ..items import RealityExecutiveItem

def get_contact_details(detail_tag):
    contact_dict = {}
    phone_list = []
    email = ''
    license = ''
    Office_no = ''
    fax = ''
    p_tag_list = detail_tag.find_all("p")
    Mobile_Phone = ''
    for p_tag in p_tag_list:
        if ":" in p_tag.text:
            try:
                contact_dict[p_tag.text.strip().split(":")[0].strip()]  = p_tag.find("span").text.strip()
            except:
                contact_dict[p_tag.text.strip().split(":")[0].strip()] = p_tag.text.strip().split(":")[1].strip()

    for key in contact_dict.keys():
        if "Phone" in key:
            phone_list.append(key+" : "+contact_dict[key])
        if "Voicemail" in key:
            phone_list.append(key+" : "+contact_dict[key])
        if "Fax" in key:
            fax = contact_dict[key]
        if "Email" in key:
            email = contact_dict[key]
        if "DRE" in key:
            license = contact_dict[key]
        if "Office" in key:
            Office_no = contact_dict[key]
        if "Mobile" in key:
            Mobile_Phone = contact_dict[key]
    other_phone = "|".join(phone_list)
    return email, license, Office_no, fax, email,other_phone, Mobile_Phone

def collect_address(detail_tag):
    streetAddress = detail_tag.find(attrs={"itemprop": "streetAddress"}).text.strip()
    addressLocality = detail_tag.find(attrs={"itemprop": "addressLocality"}).text.strip()
    addressRegion = detail_tag.find(attrs={"itemprop": "addressRegion"}).text.strip()
    postalCode = detail_tag.find(attrs={"itemprop": "postalCode"}).text.strip()
    return streetAddress, addressLocality, addressRegion, postalCode

def get_social_media(detail_tag):
    social_media_tags = detail_tag.find(class_='agent-profile-social').find_all("a")
    social_media_list = [i['href'] for i in social_media_tags]
    social_media_dict = {}
    for social_tag_url in social_media_list:
        if "facebook" in social_tag_url:
            social_media_dict['facebook'] = social_tag_url
        elif "twitter" in social_tag_url:
            social_media_dict['twitter'] = social_tag_url
        elif "linkedin" in social_tag_url:
            social_media_dict['linkedin'] = social_tag_url
        elif "youtube" in social_tag_url:
            social_media_dict['youtube'] = social_tag_url
        elif "instagram" in social_tag_url:
            social_media_dict['instagram'] = social_tag_url
        elif "pinterest" in social_tag_url:
            social_media_dict['pinterest'] = social_tag_url
        else:
            social_media_dict['other'] = social_tag_url
    try:
        facebook = social_media_dict['facebook']
    except:
        facebook = ""
    try:
        twitter = social_media_dict['twitter']
    except:
        twitter = ""
    try:
        youtube = social_media_dict['youtube']
    except:
        youtube = ""
    try:
        linkedin = social_media_dict['linkedin']
    except:
        linkedin = ""
    try:
        instagram = social_media_dict['instagram']
    except:
        instagram = ""
    try:
        pinterest = social_media_dict['pinterest']
    except:
        pinterest = ""
    agent_site = ''
    for social in social_media_tags:
        if "Blog_50X50.png" in social.find("img")['src']:
            agent_site = social['href']
    return facebook, twitter, youtube, linkedin, instagram, pinterest, agent_site

class RealtyexeSpider(scrapy.Spider):
    name = 'realtyexe'
    allowed_domains = ['realtyexecutives.com']
    start_urls = ['https://www.realtyexecutives.com/agents/us']
    def __init__(self):
        self.unique_id = 0
    def parse(self, response):
        total_agents = int(response.css('.paginationLeft::text').extract()[0].strip().split(" ")[-1])
        total_pages = int((total_agents/50)+2)
        # for page in range(1,3):
        for page in range(1,total_pages):
            page_url = "https://www.realtyexecutives.com/agents/us?page="+str(page)
            print(page_url)
            yield scrapy.Request(url=page_url,  callback=self.collect_agent_url,dont_filter = True)

    def collect_agent_url(self,response):
        container = response.css('.card-profile')
        agent_urls = ['https://www.realtyexecutives.com'+i.css('a::attr(href)').extract()[0] for i in container]
        for agent_url in agent_urls:
            yield scrapy.Request(url=agent_url,  callback=self.collect_agent_info,dont_filter = True)


    def collect_agent_info(self, response):
        agent_url = response.url
        soup = BeautifulSoup(response.text,'html.parser')
        ###############################################
        detail_tag = soup.find(class_='col-sm-5')
        ###############################################
        agent_contact_tag_list = [contact_tag['href'] for contact_tag in detail_tag.find(class_='about-button').find_all("a")[:-1]]
        try:
            agent_company_site = [company_site for company_site in agent_contact_tag_list if "http" in company_site][0]
        except:
            agent_company_site = ""
        ###############################################
        name = detail_tag.find(class_='about-name').text
        # try:
        #     mobile = detail_tag.find(id='agentDetailsPhone').text.strip()
        # except:
        #     mobile = ""
        email, license, Office_no, fax, email,other_phone ,Mobile_Phone= get_contact_details(detail_tag)
        streetAddress, addressLocality, addressRegion, postalCode = collect_address(detail_tag)
        facebook, twitter, youtube, linkedin, instagram, pinterest, agent_site = get_social_media(detail_tag)
        agent_profile_link = str(soup.find(class_='profile-img')).split("url(")[1].split("')")[0].replace("'",'')

        other_info = BeautifulSoup(str(detail_tag).split('<div itemprop="address"')[0].split("</h1>")[1].strip(),'html.parser')
        try:
            role = other_info.find("p").text
        except:
            role = ""
        try:
            office = other_info.find("div").text
        except:
            office = ""
        # if mobile=='':
        #     try:
        #         mobile = other_phone.split("|")[0].split(":")[1].strip()
        #     except:
        #         mobile = ""
        h3_tag = soup.find_all(class_='container')[-1].find_all("h3")
        h3_tag_text_list = [i.text for i in h3_tag]
        Areas_Served = ""
        Specialties = ""
        if "Areas Served" in h3_tag_text_list:
            text = str(soup).split("Areas Served")[1]
            soup_text = BeautifulSoup(text,'html.parser')
            Areas_Served = soup_text.find("p").text
        if "Specialties" in h3_tag_text_list:
            text = str(soup).split("Specialties")[1]
            soup_text = BeautifulSoup(text,'html.parser')
            Specialties = soup_text.find("p").text
        self.unique_id += 1
        item = RealityExecutiveItem()
        item['unique_id'] = "Realtyexecutives_"+str(self.unique_id)
        item['agent_url'] = agent_url
        item['agent_dp'] = agent_profile_link
        item['agent_name'] = name
        item['agent_phone'] = Mobile_Phone
        item['agent_email'] = email
        item['agent_role'] = role
        item['agent_license'] = license
        item['agent_areaserved'] = Areas_Served
        item['agent_designations'] = ''
        item['agent_facebook'] = facebook
        item['agent_instagram'] = instagram
        item['agent_twitter'] = twitter
        item['agent_linkedin'] = linkedin
        item['agent_pinterest'] = pinterest
        item['agent_youtube'] = youtube
        item['agent_site'] = agent_site
        item['agent_special_tag'] = Specialties
        item['agent_rating'] = ''
        item['office_address'] = streetAddress +" "+addressLocality+" "+addressRegion
        item['office_fax'] = fax
        item['office_branch'] = ''
        item['office_name'] = office
        item['office_phone'] = Office_no
        item['office_site'] = agent_company_site
        item['office_zip'] = postalCode
        item['office_state'] = addressRegion
        item['other_phone'] = other_phone
        item['company_facebook'] = ''
        item['company_linkedin'] = ''
        item['company_name'] = 'Realtyexecutives'
        item['company_site'] = 'https://www.realtyexecutives.com'
        item['company_twitter'] = ''
        item['date_of_data_extraction'] = datetime.now()
        item['data_extracted_by'] = 'Pooja'
        item['dataextraction_uuid'] = 'Pooja-'+datetime.now().strftime('%m-%d-%Y')

        yield item
