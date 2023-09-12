######## this code will collect all the agent links #######


# Importing libraries
import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

class AgentSpider(scrapy.Spider):
    name = 'links'
    start_urls = ['https://info.kzvth.de/ZaSuche']

#### Chromedriver Path and Headless options

    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(executable_path='chromedriver.exe',options=chrome_options)


#### Links Collection

    def parse(self,response):
        driver = self.driver
        driver.get('https://www.c21.ca/directory')
        ### Clicking tab of all links
        all_agent = driver.find_element_by_xpath(".//*[contains(concat(' ',normalize-space(@class),' '),' nav-tabs ')]//*[contains(concat(' ',normalize-space(@class),' '),' active ')]/following-sibling::*[1]/self::li//a").click()
        time.sleep(10)

        # list of links
        list_of_hrefs = []

        ### Loop over all pages

        for next_button in range(0, 842):
            try:
                content_blocks = driver.find_elements_by_class_name("aos-agent-image")
                for block in content_blocks:
                    elements = block.find_elements_by_tag_name("a")
                    for el in elements:
                        list_of_hrefs.append(el.get_attribute("href"))

                next_button = driver.find_element_by_xpath("(//span[@title='Next'])[2]").click()
                time.sleep(7)
            except:
                pass

        #### for testing, reduce the number of loop and print
        # print(*list_of_hrefs, sep='\n')

        ## Output in txt file
        with open('agent_links.txt', 'w') as f:
            for line in list_of_hrefs:
                f.write(line)
                f.write('\n')


#### to get output in txt file : scrapy crawl links