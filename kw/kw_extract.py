import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
df = pd.read_csv("kw_email_use_selenium.csv")

url_list = df['agent_url'].unique()
def get_driver():
    options = webdriver.FirefoxOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Firefox(options=options)
    return driver


def collect_agent_contact_details(driver):
    try:
        agent_info = driver.find_element_by_class_name("AgentInformation")
    except:
        agent_info = ""
    try:
        info_container = agent_info.find_elements_by_class_name("AgentInformation__factBody")
    except:
        info_container = ""
    try:
        agent_email = [email.text for email in info_container if email.get_attribute("aria-label") == 'Agent E-mail'][0]
    except:
        agent_email = ""
    try:
        mobile_number = driver.find_element_by_class_name("AgentInformation__phoneMobileNumber").text
    except:
        mobile_number = ""
    try:
        office_number = driver.find_element_by_class_name("AgentInformation__phoneOfficeNumber").text
    except:
        office_number = ""
    try:
        agent_website = [i.text for i in info_container if i.get_attribute("aria-label") == 'Agent Website'][0]
    except:
        agent_website = ""
    contact_dict = {"agent_email":agent_email,"mobile_number":mobile_number,"office_number":office_number,'agent_website':agent_website }
    return contact_dict


def get_agent_details(driver):
    try:
        agent_licenses = driver.find_element_by_class_name("AgentContent__licenses").text
    except:
        agent_licenses = ""
    try:
        agent_bio = driver.find_element_by_class_name("AgentContent__bio").text
    except:
        agent_bio = ""
    try:
        serviceAreas = driver.find_element_by_class_name("AgentContent__serviceAreas").text
    except:
        serviceAreas = ""
    try:
        agent_team_name = driver.find_element_by_class_name("AgentContent__teamName").text
    except:
        agent_team_name = ""
    try:
        agent_team_info_ = driver.find_element_by_class_name("AgentContent__teamText").text.split("\n")
        agent_team_info = ", ".join(agent_team_info_)
    except:
        agent_team_info = ""
    try:
        logo_url = driver.find_element_by_class_name('AgentContent__teamAvatar').find_element_by_class_name("KWImage__image").get_attribute("src")
    except:
        logo_url = ""
    agent_details = {"agent_licenses":agent_licenses, "agent_bio":agent_bio, "serviceAreas":serviceAreas,"agent_team_name":agent_team_name,
                    "agent_team_info":agent_team_info,'logo_url':logo_url}
    return agent_details


def social_media_details(driver):
    try:
        social_media_container = driver.find_element_by_class_name("AgentInformation__socialMedia").find_elements_by_class_name("link")
    except:
        social_media_container = []
    social_media_links = [social_media.get_attribute("href") for social_media in social_media_container]
    try:
        facebook = [facebook for facebook in social_media_links if 'facebook' in facebook][0]
    except:
        facebook = ""
    try:
        instagram = [instagram for instagram in social_media_links if 'instagram' in instagram][0]
    except:
        instagram = ""
    try:
        twitter = [twitter for twitter in social_media_links if 'twitter' in twitter][0]
    except:
        twitter = ""
    try:
        linkedin = [linkedin for linkedin in social_media_links if 'linkedin' in linkedin][0]
    except:
        linkedin = ""
    social_media_dict = {"facebook":facebook,"instagram":instagram,"twitter":twitter,"linkedin":linkedin}
    social_media_links_str = "|".join(social_media_links)
    return social_media_dict,social_media_links_str


def collect_other_info(driver):
    container = driver.find_elements_by_class_name("AgentContent__section")
    try:
        Market_Cente = [i for i in container if 'Market Center' in i.text][0].find_element_by_class_name("AgentContent__sectionText").text
    except:
        Market_Cente = ""
    try:
        Languages = [i for i in container if 'Languages' in i.text][0].find_element_by_class_name("AgentContent__sectionText").text
    except:
        Languages = ""
    try:
        Specialties_designation = [i for i in container if 'Specialties and Designations' in i.text][0].find_element_by_class_name("AgentContent__sectionText").text
    except:
        Specialties_designation = ""
    other_info = {"Market_Cente":Market_Cente, "Languages":Languages, "Specialties_Designations":Specialties_designation}
    return other_info

def wait_to_page_load(driver):
    try:
        w = WebDriverWait(driver, 3)
        w.until(EC.presence_of_element_located((By.CLASS_NAME,"AgentContent__name")))
        print("Page load happened")
    except Exception as e:
        print("Timeout happened no page load")
    return driver

url_count = 40255
driver_count = 0
driver = get_driver()
for url in url_list[url_count:50000]:
    print(url)
    if driver_count >=100:
        print("need to close driver")
        driver.quit()
        driver_count = 0
        driver = get_driver()
        print("new driver initialize****************")
    driver.get(url)
    driver = wait_to_page_load(driver)
    try:
        agent_name = driver.find_element_by_class_name("AgentContent__name").text
    except:
        agent_name = ""
    try:
        time.sleep(0.5)
        profile_url = driver.find_element_by_class_name("AvatarImage__bg").get_attribute("style").replace('background-image: url("','').replace('");','')
    except:
        profile_url = ""
    try:
        tag = driver.find_element_by_class_name("pill").text
    except:
        tag = ""
    try:
        role = driver.find_element_by_class_name("AgentContent__team").text
    except:
        role = ""
    try:
        location = driver.find_element_by_class_name("AgentContent__location").text
    except:
        location = ""
    contact_dict = collect_agent_contact_details(driver)
    agent_details = get_agent_details(driver)
    social_media_dict,social_media_links_str = social_media_details(driver)
    other_info = collect_other_info(driver)
    data_dict = {'agent_url':url,"agent_name":agent_name, 'agent_role':role,'location':location,"agent_dp":profile_url, "tag":tag,"agent_email":contact_dict['agent_email'], "mobile_number":contact_dict['mobile_number'],"office_number":contact_dict['office_number'],'agent_license':agent_details['agent_licenses'], 'agent_bio':agent_details['agent_bio'],'serviceAreas':agent_details['serviceAreas'],'office_name':agent_details['agent_team_name'],'office_address':agent_details['agent_team_info'],'logo_url':agent_details['logo_url'],'facebook':social_media_dict['facebook'], 'instagram':social_media_dict['instagram'],'twitter':social_media_dict['twitter'],'linkedin':social_media_dict['linkedin'],'Market_Cente':other_info['Market_Cente'],'agent_language':other_info['Languages'],'Specialties_Designations':other_info['Specialties_Designations'],'social_media_links_str':social_media_links_str,'agent_website':contact_dict['agent_website']}
    data_df = pd.DataFrame(data_dict,index=[0],columns=['agent_url','agent_name', 'agent_role','location','agent_dp', 'tag','agent_email', 'mobile_number','office_number', 'agent_license', 'agent_bio', 'serviceAreas','office_name', 'office_address','logo_url','facebook', 'instagram', 'twitter', 'linkedin','Market_Cente', 'agent_language', 'Specialties_Designations','social_media_links_str','agent_website'])
    with open("kw_data-emailSelenium.csv",'a',newline='',encoding='utf-8') as f:
        data_df.to_csv(f, mode='a',header=f.tell()==0)
    print(url_count,url)
    url_count+=1
    driver_count+=1
    print("***********************************")
driver.quit()
