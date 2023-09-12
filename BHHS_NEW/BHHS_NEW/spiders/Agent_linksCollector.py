import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from shutil import which
from time import sleep
class AgentLinkscollectorSpider(scrapy.Spider):
    name = 'Agent_linksCollector'
    allowed_domains = ['www.bhhs.com']
    start_urls = ['http://www.bhhs.com/']
    def __init__(self):
        # chrome_options = Options()
        # chrome_options.add_argument('headless')
        chrome_path = which(r'/home/bharath/Desktop/phone_number_bot/chromedriver')
        self.driv = webdriver.Chrome(executable_path=chrome_path)
        # self.driv = webdriver.Chrome(executable_path=chrome_path,chrome_options =chrome_options )
    def parse(self, response):
        driver = self.driv
        driver.get('https://www.bhhs.com/agent-search-results')
        ######### drop down####################
        sleep(3)
        # driver.find_element_by_xpath('//section[@class="cmp-dropdown compact"]/div/select/option[@value="50"]').click()
        # sleep(2)
        while True:
            links = driver.find_elements_by_xpath('//div[@class="col-6 col-sm-4 col-lg-3 order-lg-3 associate__btn-group"]/section[2]/a')
            for link in links:
                yield{
                'links':'https://www.bhhs.com'+str(link.get_attribute('href'))
                }
            sleep(3)
            next = driver.find_element_by_xpath('//a[@class="cmp-search-results-pagination__arrow cmp-search-results-pagination__arrow--next d-none d-lg-inline-block"]')
            next.click()
            sleep(5)
            if not next:
                break
