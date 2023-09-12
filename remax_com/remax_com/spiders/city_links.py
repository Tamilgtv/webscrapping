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
from time import sleep
import re
################################# For collecting city links#########################
class CityLinksSpider(scrapy.Spider):
    name = 'city_links'
    allowed_domains = ['www.remax.com']
    start_urls = ['https://www.remax.com/real-estate-agents']
    def __init__(self):
        chrome_path = which("chromedriver")
        self.driv = webdriver.Chrome(executable_path=chrome_path)


    def parse(self, response):
        driver = self.driv
        city_links = pd.read_excel('city_links.xlsx')
        for i in range (0,len(city_links['city'])):
        # for i in range (1,2):
            # driver.get(str(city_links['city_links'][i]))
            name=[]
            driver.get('https://www.remax.com/real-estate-agents')
            try:
                if driver.find_element_by_xpath('//*[@id="__layout"]/div/div[1]/div/div[2]/button/div'):
                    driver.find_element_by_xpath('//*[@id="__layout"]/div/div[1]/div/div[2]/button/div').click()
                    print('cookies_accepted')
                else:
                    print('already_accepted')
            except:
                pass
            sleep(2)   
            driver.find_element_by_xpath('//input[@class="search places-only br-none"]').send_keys(city_links['city'][i])
            sleep(20)
            self.html = driver.page_source
            resp = Selector(text=self.html)
            for i in resp.xpath('//div[@class="mb-2 pl-12 pr-4 cursor-pointer autocomplete-result hover:bg-grey-lighter"]/small'):
                yield{
                    'city-links':"https://www.remax.com/real-estate-agents/"+(str(i.xpath('normalize-space(.//text())').get()).lower()).replace(',',"").replace(" ","-")+'?count=96&sortBy=firstName'
                }
            sleep(2)
            driver.find_element_by_xpath('//input[@class="search places-only br-none"]').clear()
            sleep(2)
