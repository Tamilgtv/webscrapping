# -*- coding: utf-8 -*-
import scrapy
import scrapy
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options

from datetime import datetime
import psycopg2.extras as extras
from datetime import date
import psycopg2
import numpy as np
import time
options = Options()
options.add_extension(r'D:/Tamil/chrome driver/tb.crx')
connection = psycopg2.connect(user='postgres',
                              password='tamil',
                              host='localhost',
                              port=5432,
                              database='DMP')
cursor = connection.cursor()
driver = webdriver.Chrome(executable_path='D:/Tamil/chrome driver/chromedriver.exe',chrome_options=options)

class HomesmartSpider(scrapy.Spider):
    name = 'homesmart'
    allowed_domains = ['homesmart.com']
    # start_urls = ['http://homesmart.com/']
    

    def parse(self, response):
        
        def execute_values(conn, df, table):
            # Create a list of tupples from the dataframe values
            tuples = [tuple(x) for x in df.to_numpy()]
            # Comma-separated dataframe columns
            cols = ','.join(list(df.columns))
            # SQL query to execute
            query  = "INSERT INTO %s(%s) VALUES %%s;" % (table, cols)
            cursor = conn.cursor()
            try:
                extras.execute_values(cursor, query, tuples)
                conn.commit()
            except (Exception, psycopg2.DatabaseError) as error:
                print("Error: %s" % error)
                conn.rollback()
                cursor.close()
                return 1
            print("execute_values() done")
            cursor.close()
            conn.close()
        
        # item = items.HomesmartNewItem()
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
        
        #driver = webdriver.Chrome(executable_path='D:/Tamil/chrome driver/chromedriver.exe',chrome_options=options)
        user_input = input("enter ok")
        driver.get('https://homesmart.com/officesagents/search-agents/?userSearch=&officeSearch=&citySearch=&stateSearch=ALL&areaSearch=&desigFld=&hobbiesFld=&specialtyFld=&civicFld=&LanguagesSEL=&button=Search')
        
        ##### Looping in different States
        z = 0
        df = pd.DataFrame([])
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
                            
                        df.loc[z,'agent_url'] = ''
                        df.loc[z,'agent_dp'] = image
                        df.loc[z,'agent_name'] = name
                        df.loc[z,'agent_phone'] = mobile.replace('Mobile:','').replace('Direct:','').replace('-','').replace('(','').replace(')','').replace(' ','')
                        df.loc[z,'agent_email'] = email
                        df.loc[z,'agent_role'] = 'Agent'
                        df.loc[z,'agent_license'] = agent_license.strip()
                        df.loc[z,'agent_areaserved'] = area_served.replace('Service Area(s):','').strip()
                        df.loc[z,'agent_designation'] = designation.strip()
                        df.loc[z,'agent_facebook'] = facebook
                        df.loc[z,'agent_instagram'] = ''
                        df.loc[z,'agent_twitter'] = twitter
                        df.loc[z,'agent_linkedin'] = linkedin
                        df.loc[z,'agent_pinterest'] = ''
                        df.loc[z,'agent_youtube'] = ''
                        df.loc[z,'agent_site'] = agent_website
                        df.loc[z,'agent_special_tag'] = ''
                        df.loc[z,'agent_rating'] = ''
                        df.loc[z,'office_address'] = address.replace('Address:','').strip()
                        df.loc[z,'office_fax'] = ''
                        df.loc[z,'office_branch'] = ''
                        df.loc[z,'office_name'] = office_name.replace('Office:','').strip()
                        df.loc[z,'office_phone'] = office_no
                        df.loc[z,'office_site'] = ''
                        df.loc[z,'office_zip'] = Zip
                        df.loc[z,'office_state'] = state
                        df.loc[z,'other_phone'] = ''
                        df.loc[z,'company_facebook'] = ''
                        df.loc[z,'company_linkedin'] = ''
                        df.loc[z,'company_name'] = 'HOMESMART'
                        df.loc[z,'company_site'] = 'https://homesmart.com/'
                        df.loc[z,'company_twitter'] = ''
                        df.loc[z,'date_of_data_extraction'] = datetime.now()
                        df.loc[z,'data_extracted_by'] = 'Tamil'
                        df.loc[z,'dataextraction_uuid'] = ''
                        df.loc[z,'datacleaned_uuid'] = ''
                        df.loc[z,'uploading'] = ''
                        
                        z = z+1
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
        
        df2 = df.copy()
        print(len(df2))
        ###### Get output file in csv
        #df.to_csv('homesmart_clean.csv', index=False,header=True, encoding='utf-8')
        df2 = df2[(df2['agent_name'].notna()) & (df2['agent_name'] != '')]
        execute_values(connection,df2, 'internal_data_exctraction')
        print(len(df2), 'records executed')
        