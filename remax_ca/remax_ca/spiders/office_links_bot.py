import scrapy
from shutil import which
from time import sleep
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys


class OfficeLinksBotSpider(scrapy.Spider):
    name = 'office_links_bot'
    allowed_domains = ['www.remax.com']
    start_urls =['https://www.remax.ca/real-estate-agents-in-canada']
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument('headless')

        chrome_path = which("chromedriver")

        self.driv = webdriver.Chrome(executable_path=chrome_path, options=chrome_options)
    # def start_requests(self):
    #     yield scrapy.Request(url='https://www.remax.ca/real-estate-agents-in-canada', callback=self.parse,headers= {
    #             'user_agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
    #         }) 

    def parse(self, response):
        
        driver = self.driv
        driver.get('https://www.remax.ca/real-estate-agents-in-canada')
        sleep(2)
        expander = driver.find_elements_by_xpath('//span[@class="material-icons"]')
        print(len(expander))
        for exp in expander:
            sleep(2)
            exp.click()
        self.html = driver.page_source
        resp = Selector(text=self.html)
        print(resp)
        links = resp.xpath('//div[@class="link-card-container"]/div[1]/a/@href').getall()
        
        #Extracting Office Links
        for link in links:
            yield{
                'Links':'https://www.remax.ca/'+str(link)
            }
