import scrapy
import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

import time


names = []
images = []
emails = []
mobiles = []
office_names = []
addresses = []
office_nos = []
area_serveds = []
agent_licenses = []
agent_websites = []
designations = []
Agent_facebook = []
Agent_twitter = []
Agent_linkedin = []


class Agent_Spider(scrapy.Spider):
    name = 'homesmart'
    #start_urls = ['https://info.kzvth.de/ZaSuche']

#### chromedriver path and headless options

    def __init__(self):
        # chrome_options = Options()
        # chrome_options.add_argument("--headless")
        # chrome_options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(executable_path='D:/Tamil/chrome driver/chromedriver.exe')


#### Links Collection

    def parse(self,response):
        driver = self.driver
        driver.get('https://homesmart.com/officesagents/search-agents/?userSearch=&officeSearch=&citySearch=&stateSearch=ALL&areaSearch=&desigFld=&hobbiesFld=&specialtyFld=&civicFld=&LanguagesSEL=&button=Search')

##### Looping in different States
        for i in range(2, 4):
            ele_state = driver.find_element(By.ID, 'stateSearch')
            select = Select(ele_state)
            select.select_by_index(i)
         ## Clicking Search Button
            searchbutton = driver.find_element_by_id("button")
            driver.execute_script("arguments[0].click();", searchbutton)


###### Looping Individual Page
            for data in range(2, 27):
                try:
                    try:
                        agent = driver.find_element_by_xpath("//div[@id='agent-contatainer']/table/tbody/tr"'[' + str(data) + ']'"/td[3]")
                        driver.execute_script("arguments[0].click();", agent)
                    except:
                        pass
                ### Clicking Iframe of Agent
                    try:
                        iframe = driver.find_element_by_xpath('//*[@class="fancybox-iframe"]')
                        driver.switch_to.frame(iframe)
                    except:
                        pass
                ### Extracting Information of Agents
                    try:
                        name = driver.find_element_by_class_name("agentName")
                    except:
                        pass
                    try:
                        image = driver.find_element_by_xpath("/html/body/div/table/tbody/tr[2]/td[1]/img")
                    except:
                        pass

                    try:
                        email = driver.find_element_by_xpath("/html/body/div/div[1]/a")
                    except:
                        pass
                    try:
                        mobile = driver.find_element_by_xpath("//*[@id='phone']")
                    except:
                        pass
                    try:
                        office_name = driver.find_element_by_xpath("/html/body/div/table/tbody/tr[2]/td[2]/div[1]")
                    except:
                        pass
                    try:
                        address = driver.find_element_by_xpath("/html/body/div/table/tbody/tr[2]/td[2]/div[2]")
                    except:
                        pass
                    try:
                        office_no = driver.find_element_by_xpath("/html/body/div/table/tbody/tr[2]/td[2]/div[3]")
                    except:
                        pass
                    try:
                        area_served = driver.find_element_by_xpath("/html/body/div/table/tbody/tr[2]/td[2]/div[4]")
                    except:
                        pass
                    try:
                        agent_website = driver.find_element_by_xpath("/html/body/div/table/tbody/tr[1]/td/ul/li[1]/a")
                    except:
                        pass
                    try:
                        agent_license = driver.find_element_by_xpath("/html/body/div/table/tbody/tr[2]/td[2]/div[5]")
                    except:
                        pass
                    try:
                        designation = driver.find_element_by_xpath("/html/body/div/div[4]/label[contains(text(),'Designations:')]/..")
                    except:
                        pass
                    try:
                        facebook = driver.find_element_by_xpath("/html/body/div/table/tbody/tr[1]/td/ul/li[4]/a")
                    except:
                        pass
                    try:
                        twitter = driver.find_element_by_xpath("/html/body/div/table/tbody/tr[1]/td/ul/li[5]/a")
                    except:
                        pass
                    try:
                        linkedin = driver.find_element_by_xpath("/html/body/div/table/tbody/tr[1]/td/ul/li[6]/a")
                    except:
                        pass

####### Appending Values to List

                    try:
                        names.append(name.text)
                    except:
                        names.append("")
                    try:
                        images.append(image.get_attribute('src'))
                    except:
                        images.append("")
                    try:
                        emails.append(email.text)
                    except:
                        emails.append("")
                    try:
                        mobiles.append(mobile.text)
                    except:
                        mobiles.append("")
                    try:
                        office_names.append(office_name.text)
                    except:
                        office_names.append("")
                    try:
                        addresses.append(address.text)
                    except:
                        addresses.append("")
                    try:
                        office_nos.append(office_no.text)
                    except:
                        office_nos.append("")
                    try:
                        area_serveds.append(area_served.text)
                    except:
                        area_serveds.append("")
                    try:
                        agent_licenses.append(agent_license.text)
                    except:
                        agent_licenses.append("")
                    try:
                        agent_websites.append(agent_website.get_attribute('href'))
                    except:
                        agent_websites.append("")
                    try:
                        designations.append(designation.text)
                    except:
                        designations.append("")
                    try:
                        Agent_facebook.append(facebook.get_attribute('href'))
                    except:
                        Agent_facebook.append("")
                    try:
                        Agent_twitter.append(twitter.get_attribute('href'))
                    except:
                        Agent_twitter.append("")
                    try:
                        Agent_linkedin.append(linkedin.get_attribute('href'))
                    except:
                        Agent_linkedin.append("")
                    driver.switch_to.default_content()

                    data += 1
                    time.sleep(3)
                except:
                    pass

###### CLicking Next Button
            try:
                next = driver.find_element_by_link_text("Next")
                driver.execute_script("arguments[0].click();", next)
            except:
                pass


        data={
                   'Agent_Name':names,
                    'Agent_DP':images,
                    'Agent_Phone':mobiles,
                    'Agent_Email':emails,

                    'Agent_License':agent_licenses,
                    'Agent_AreaServed':area_serveds,
                    'Agent_Designation':designations,
                    'Agent_Facebook':Agent_facebook,
                   'Agent_Linkedin':Agent_linkedin,

                    'Agent_Twitter':Agent_twitter,
                    'Agent_Site':agent_websites,
                    'Office_Address':addresses,
                    'Office_Name':office_names,
                    'Office_Phone':office_nos

        }

        df=pd.DataFrame.from_dict(data, orient='index')
        df = df.transpose()

##### Cleaning Dataset
        df['Agent_Phone']=df['Agent_Phone'].astype(str).str.replace(r'Mobile:', '')
        df['Agent_Phone']=df['Agent_Phone'].astype(str).str.replace(r'Direct:', '')
        df['Office_Address']=df['Office_Address'].astype(str).str.replace(r'Address:', '')
        df['Office_Name']=df['Office_Name'].astype(str).str.replace(r'Office:', '')
        df['Agent_Designation']=df['Agent_Designation'].astype(str).str.replace(r'Designations: ', '')
        df['Office_Phone']=df['Office_Phone'].astype(str).str.replace(r'Office Phone:', '')
        df['Agent_License'] = df['Agent_License'].replace(r'^([^0-9]*)$',np.nan, regex=True)
        df['Agent_License'] = df['Agent_License'].dropna()
        df['Zipcode']=df['Office_Address'].astype(str).str.split().str[-1]
        df['Agent_AreaServed']=df['Agent_AreaServed'].astype(str).str.replace(r'Location:', '')


###### Get output file in csv
        df.to_csv('homesmart_clean.csv', index=False,header=True, encoding='utf-8')



##### to get the output in csv file: scrapy crawl homesmart
