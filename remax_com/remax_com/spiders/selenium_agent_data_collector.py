import scrapy
from scrapy.selector import Selector
from selenium import webdriver
import pandas as pd
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from shutil import which
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from selenium.common.exceptions import StaleElementReferenceException
import json
from tqdm import tqdm
class SelSpider(scrapy.Spider):
    name = 'sel'
    allowed_domains = ['www.remax.com']
    start_urls = ['https://www.remax.com/real-estate-agents/california-md?sortBy=firstName']
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36')
        chrome_path = which("chromedriver")
        self.driv = webdriver.Chrome(executable_path=chrome_path, options=chrome_options)

    def parse(self, response):
        driver = self.driv
        names =pd.read_excel('agent_names.xlsx')
        # driver.get('https://www.remax.com/real-estate-agents')
        for name in names['Name']:
            driver.get('https://www.remax.com/real-estate-agents')
            # try:
            #     WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[@class="dbutton_2pUfk dbutton--secondary_1CoUL"]'))).click()
            # except:
            #     pass
            # # driver.find_element_by_xpath('//button[@class="dbutton_2pUfk dbutton--secondary_1CoUL"]').click() #clicking on cookies button
            sleep(3) 
            nam = driver.find_element_by_xpath('//input[@id="Agent-Name"]').send_keys(str(name))
            
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[@class="form-button w-full secondary"]'))).click()
            
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(2)
            try:
                WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '(//div[@class="imageContainer"])[1]'))).click()
            except:
                pass
            
            # driver.execute_script("window.scrollTo(0, 800);")
            # driver.find_element_by_xpath('(//div[@class="imageContainer"])[1]').click()
            sleep(10)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # self.html = driver.page_source
            resp = Selector(text=driver.page_source)
            try:
                WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="noprint"]/h1'))).click()
            except:
                pass
            # WebDriverWait(driver, 10).until(element_present)
            Agent_DP = resp.xpath('//div[@class="col md:max-w-1/2 lg:max-w-full"]/img/@src').get(default = "")
            Agent_Name =resp.xpath('normalize-space(//div[@class="noprint"]/h1/text())').get(default="")
            Agent_Phone1= resp.xpath('normalize-space((//div[@class="bio-phone mb-8 lg:mb-0"]/h4/span/a/text())[1])').get(default = "")
            Agent_Phone2= resp.xpath('normalize-space((//div[@class="bio-phone mb-8 lg:mb-0"]/h4/span/a/text())[2])').get(default = "")
            Agent_Phone3 = resp.xpath('normalize-space((//div[@class="bio-phone mb-8 lg:mb-0"]/h4/span/a/text())[3])').get(default = "")
            Agent_Role= resp.xpath('normalize-space(//div[@class="mt-2"]/h6/span/text())').get(default = "")
            Agent_License= resp.xpath('normalize-space(//div[@class="mt-2"]/h6/span[2]/text())').get(default = "")
            Agent_Designation = resp.xpath('(//div[@class="col md:max-w-1/2 lg:max-w-full"])[2]').get(default = "")
            Agent_Facebook= resp.xpath('//div[@class="mb-12"]/a[@aria-label="RE/MAX on FACEBOOK"]/@href').get(default="")
            Agent_Linkedin =resp.xpath('//div[@class="mb-12"]/a[@aria-label="RE/MAX on LINKEDIN"]/@href').get(default="")
            Agent_instagram= resp.xpath('//div[@class="mb-12"]/a[@aria-label="RE/MAX on INSTAGRAM"]/@href').get(default="")
            Agent_website= resp.xpath('//div[@class="w-full"]/a/@href').get(default="")
            Office_address= resp.xpath('normalize-space(//a[@class="inline-block directions-link"])').extract_first(default="")
            office_Name= resp.xpath('normalize-space(//h4[@class="mb-2"]/a/text())').get(default="")
            Office_Website= 'https://www.remax.com/'+str(resp.xpath('//h4[@class="mb-2"]/a/@href').get(default=""))    

            yield{
                        'Agent_url': driver.current_url,
                        'Agent_DP': Agent_DP,
                        'Agent_Name': Agent_Name,
                        'Agent_Phone1':Agent_Phone1,
                        'Agent_Phone2': Agent_Phone2,
                        'Agent_Phone3': Agent_Phone3,
                        'Agent_Role': Agent_Role ,
                        'Agent_License': Agent_License,
                        'Agent_Designation': Agent_Designation,
                        'Agent_Facebook': Agent_Facebook,
                        'Agent_Linkedin':Agent_Linkedin,
                        'Agent_instagram': Agent_instagram,
                        'Agent_website': Agent_website,
                        'About': resp.xpath('normalize-space((//div[@class="row"])[2])').extract(),
                        'Office_address': Office_address,
                        'office_Name': office_Name,
                        'Office_Website': Office_Website


                    }
            sleep(5)
            