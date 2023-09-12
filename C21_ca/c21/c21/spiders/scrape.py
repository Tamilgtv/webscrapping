######## this code will collect information from all the links ######


import scrapy

class AgentsSpider(scrapy.Spider):
    name = 'agents'

# Here we are reading the agent links file
    with open('agent_links.txt') as f:
        start_urls = [line.strip() for line in f]

# Here we are parsing each Agent Link to collect Information

    def parse(self, response):

        address = list(filter(None, [
                text.get().replace('\n', '').strip()
                for text in
                response.css('div[class="aos-agent-office-meta-detail margin-left-right-streach-15"] ::text')
            ]))[0:5]
        zipcode = response.xpath("//*[@class='aos-agent-office-location-city-state-zip']/text()").get()


        yield {
            'Agent_URL' : response.url,
             'Agent_DP' :response.xpath("//*[@class='aos-agent-image']/img/@src").get(),
            'Agent_Name' :response.css("h1.aos-agent-display-name::text").get().split(),

            'Agent_Main' :response.xpath("//*[contains(text(),'Main')]/following-sibling::a/text()").get(),
            'Agent_Cell': response.xpath("//*[contains(text(),'Cell')]/following-sibling::a/text()").get(),
            'Agent_Office': response.xpath("//*[contains(text(),'Office')]/following-sibling::a/text()").get(),
            'Agent_Email' : response.xpath("//*[contains(text(),'Email')]/following-sibling::a/text()").get(),
            'Agent_Role' : response.css("div.aos-agent-licensing-info p::text").get(),

            'Agent_Designation': response.css(".aos-agent-licensing-info p+ p::text").get(),
            'Agent_Facebook':
                response.css(".aos-agent-social-media-icon-facebook::attr(href)").extract(),
            'Agent_Linkedln':
                response.css(".aos-agent-social-media-icon-linkedin::attr(href)").get(),
            'Agent_Instagram':
                response.css(".aos-agent-social-media-icon-instagram::attr(href)").get(),
            'Agent_Twitter':
                response.xpath("//*[@class=' aos-agent-social-media-icon-twitter']/@href").get(),

            'Company_Site': response.xpath("//*[contains(text(),'Website')]/following-sibling::a/text()").get(),
            'Office_Name': response.css(".aos-agent-office-display-name a::text").get(),
            'Office_Address': address,
            'Office_Zip': zipcode[-10:]
        }


### get the output in csv file using: scrapy crawl agents -O (filename).csv