# -*- coding: utf-8 -*-
import scrapy
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from homesmart_new import items
from datetime import datetime
import numpy as np
import time
options = Options()
options.add_extension(r'D:/Tamil/chrome driver/tb.crx')

class HomesmartSpider(scrapy.Spider):
    name = 'homesmart'
    #allowed_domains = ['homesmart.com']
    #start_urls = ['http://homesmart.com/']

    def parse(self, response):
        
        item = items.HomesmartNewItem()
        # names = []
        # images = []
        # emails = []
        # mobiles = []
        # office_names = []
        # addresses = []
        # office_nos = []
        # area_serveds = []
        # agent_licenses = []
        # agent_websites = []
        # designations = []
        # Agent_facebook = []
        # Agent_twitter = []
        # Agent_linkedin = []
        
        driver = webdriver.Chrome(executable_path='D:/Tamil/chrome driver/chromedriver.exe',chrome_options=options)
        user_input = input("enter ok")
        driver.get('https://homesmart.com/officesagents/search-agents/?userSearch=&officeSearch=&citySearch=&stateSearch=ALL&areaSearch=&desigFld=&hobbiesFld=&specialtyFld=&civicFld=&LanguagesSEL=&button=Search')
        
        ##### Looping in different States
        for i in range(3, 4):
            ele_state = driver.find_element(By.ID, 'stateSearch')
            select = Select(ele_state)
            select.select_by_index(i)
         ## Clicking Search Button
            searchbutton = driver.find_element_by_id("button")
            driver.execute_script("arguments[0].click();", searchbutton)
        
        
        ###### Looping Individual Page
            for page in range(1, 3):
            #while True:
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
                            name = name.text
                        except:
                            name = ''
                            pass
                        try:
                            image = driver.find_element_by_xpath("/html/body/div/table/tbody/tr[2]/td[1]/img")
                            image = image.get_attribute('src')
                        except:
                            image = ''
                            pass
        
                        try:
                            email = driver.find_element_by_xpath("/html/body/div/div[1]/a")
                            email = email.text
                        except:
                            email = ''
                            pass
                        try:
                            mobile = driver.find_element_by_xpath("//*[@id='phone']")
                            mobile = mobile.text
                        except:
                            mobile = ''
                            pass
                        
                        try:
                            #office_name = driver.find_element_by_xpath("/html/body/div/table/tbody/tr[2]/td[2]/div[1]")
                            office_name = ''.join([x.text for x in  driver.find_elements_by_xpath('//td/div') if 'Office' in x.text ])
                        except:
                            office_name = ''
                            pass
                        try:
                            #address = driver.find_element_by_xpath("/html/body/div/table/tbody/tr[2]/td[2]/div[2]")
                            address = ''.join([x.text for x in  driver.find_elements_by_xpath('//td/div') if 'Address:' in x.text ])
                        except:
                            address = ''
                            
                            pass
                        try:
                            #office_no = driver.find_element_by_xpath("/html/body/div/table/tbody/tr[2]/td[2]/div[3]")
                            office_no = ''.join([x.text for x in  driver.find_elements_by_xpath('//td/div') if 'Office Phone' in x.text])
                            office_no = office_no.replace('Office Phone:','')
                        except:
                            office_no = ''
                            pass
                        try:
                            #area_served = driver.find_element_by_xpath("/html/body/div/table/tbody/tr[2]/td[2]/div[4]")
                            area_served =  ''.join([x.text for x in  driver.find_elements_by_xpath('//td/div') if 'Service' in x.text])
                            if area_served == '':
                                area_served =  ''.join([x.text for x in  driver.find_elements_by_xpath('//td/div') if 'Location' in x.text])
                            area_served = area_served.replace('Location:','').replace('Service Area(s):','').strip()
                        except:
                            area_served =''
                            pass
                        try:
                            agent_website = driver.find_element_by_xpath("/html/body/div/table/tbody/tr[1]/td/ul/li[1]/a")
                            agent_website = agent_website.get_attribute('href')
                        except:
                            agent_website = ''
                            pass
                        try:
                            #agent_license = driver.find_element_by_xpath("/html/body/div/table/tbody/tr[2]/td[2]/div[5]")
                            agent_license = ''.join([x.text for x in  driver.find_elements_by_xpath('//td/div') if 'DRE' in x.text ])
                            agent_license = agent_license.replace('DRE:','')
                        except:
                            agent_license= ''
                            pass
                        try:
                            designation = driver.find_element_by_xpath("/html/body/div/div[4]/label[contains(text(),'Designations:')]/..")
                            designation = designation.text 
                            designation = designation.replace('Designations:','')
                        except:
                            designation = ''
                            pass
                        try:
                            facebook = driver.find_element_by_xpath("/html/body/div/table/tbody/tr[1]/td/ul/li[4]/a")
                            facebook = facebook.get_attribute('href')
                        except:
                            facebook = ''
                            pass
                        try:
                            twitter = driver.find_element_by_xpath("/html/body/div/table/tbody/tr[1]/td/ul/li[5]/a")
                            twitter = twitter.get_attribute('href')
                        except:
                            twitter = ''
                            pass
                        try:
                            linkedin = driver.find_element_by_xpath("/html/body/div/table/tbody/tr[1]/td/ul/li[6]/a")
                            linkedin = linkedin.get_attribute('href')
                        except:
                            linkedin = ''
                            pass
        
            ####### Appending Values to List
        
                        # try:
                        #     names.append(name)
                        # except:
                        #     names.append("")
                        # try:
                        #     images.append(image)
                        # except:
                        #     images.append("")
                        # try:
                        #     emails.append(email)
                        # except:
                        #     emails.append("")
                        # try:
                        #     mobiles.append(mobile)
                        # except:
                        #     mobiles.append("")
                        # try:
                        #     office_names.append(office_name)
                        # except:
                        #     office_names.append("")
                        # try:
                        #     addresses.append(address)
                        # except:
                        #     addresses.append("")
                        # try:
                        #     office_nos.append(office_no)
                        # except:
                        #     office_nos.append("")
                        # try:
                        #     area_serveds.append(area_served)
                        # except:
                        #     area_serveds.append("")
                        # try:
                        #     agent_licenses.append(agent_license)
                        # except:
                        #     agent_licenses.append("")
                        # try:
                        #     agent_websites.append(agent_website)
                        # except:
                        #     agent_websites.append("")
                        # try:
                        #     designations.append(designation)
                        # except:
                        #     designations.append("")
                        # try:
                        #     Agent_facebook.append(facebook)
                        # except:
                        #     Agent_facebook.append("")
                        # try:
                        #     Agent_twitter.append(twitter)
                        # except:
                        #     Agent_twitter.append("")
                        # try:
                        #     Agent_linkedin.append(linkedin)
                        # except:
                        #     Agent_linkedin.append("")
                        
                        driver.switch_to.default_content()
                        
                        try:
                            Zip = address.split(' ')[-1]
                        except:
                            Zip = ''
                            
                        try:
                            state = address.split(' ')[-2]
                        except:
                            state = ''
                            
                        item['agent_url'] = ''
                        item['agent_dp'] = image
                        item['agent_name'] = name
                        item['agent_phone'] = mobile.replace('Mobile:','').replace('Direct:','').replace('-','').replace('(','').replace(')','').replace(' ','')
                        item['agent_email'] = email
                        item['agent_role'] = 'Agent'
                        item['agent_license'] = agent_license.strip()
                        item['agent_areaserved'] = area_served.replace('Service Area(s):','').strip()
                        item['agent_designation'] = designation.strip()
                        item['agent_facebook'] = facebook
                        item['agent_instagram'] = ''
                        item['agent_twitter'] = twitter
                        item['agent_linkedin'] = linkedin
                        item['agent_pinterest'] = ''
                        item['agent_youtube'] = ''
                        item['agent_site'] = agent_website
                        item['agent_special_tag'] = ''
                        item['agent_rating'] = ''
                        item['office_address'] = address.replace('Address:','').strip()
                        item['office_fax'] = ''
                        item['office_branch'] = ''
                        item['office_name'] = office_name.replace('Office:','').strip()
                        item['office_phone'] = office_no
                        item['office_site'] = ''
                        item['office_zip'] = Zip
                        item['office_state'] = state
                        item['other_phone'] = ''
                        item['company_facebook'] = ''
                        item['company_linkedin'] = ''
                        item['company_name'] = 'HOMESMART'
                        item['company_site'] = 'https://homesmart.com'
                        item['company_twitter'] = ''
                        item['date_of_data_extraction'] = datetime.now()
                        item['data_extracted_by'] = 'Tamil'
                        item['dataextraction_uuid'] = ''
                        item['datacleaned_uuid'] = ''
                        item['uploading'] = ''
                        
                        data += 1
                        time.sleep(3)
                        
                    except:
                        pass
        
            ###### CLicking Next Button
                try:
                    Next = driver.find_element_by_link_text("Next")
                    driver.execute_script("arguments[0].click();", Next)
                except:
                    break
                    pass
        
        
        # data={
        #            'Agent_Name':names,
        #             'Agent_DP':images,
        #             'Agent_Phone':mobiles,
        #             'Agent_Email':emails,
        
        #             'Agent_License':agent_licenses,
        #             'Agent_AreaServed':area_serveds,
        #             'Agent_Designation':designations,
        #             'Agent_Facebook':Agent_facebook,
        #            'Agent_Linkedin':Agent_linkedin,
        
        #             'Agent_Twitter':Agent_twitter,
        #             'Agent_Site':agent_websites,
        #             'Office_Address':addresses,
        #             'Office_Name':office_names,
        #             'Office_Phone':office_nos
        
        # }
        
        # df=pd.DataFrame.from_dict(data, orient='index')
        # df = df.transpose()
        
        # ##### Cleaning Dataset
        # df['Agent_Phone']=df['Agent_Phone'].astype(str).str.replace(r'Mobile:', '')
        # df['Agent_Phone']=df['Agent_Phone'].astype(str).str.replace(r'Direct:', '')
        # df['Office_Address']=df['Office_Address'].astype(str).str.replace(r'Address:', '')
        # df['Office_Name']=df['Office_Name'].astype(str).str.replace(r'Office:', '')
        # df['Agent_Designation']=df['Agent_Designation'].astype(str).str.replace(r'Designations: ', '')
        # df['Office_Phone']=df['Office_Phone'].astype(str).str.replace(r'Office Phone:', '')
        # df['Agent_License'] = df['Agent_License'].replace(r'^([^0-9]*)$',np.nan, regex=True)
        # df['Agent_License'] = df['Agent_License'].dropna()
        # df['Zipcode']=df['Office_Address'].astype(str).str.split().str[-1]
        # df['Agent_AreaServed']=df['Agent_AreaServed'].astype(str).str.replace(r'Service Area(s):', '')
        
        
        ###### Get output file in csv
        #df.to_csv('homesmart_clean.csv', index=False,header=True, encoding='utf-8')
        
                
        
