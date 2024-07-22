import scrapy
import random 
from F1_WebScrape.items import Stories


class F1Spider(scrapy.Spider):
    name = "F1"
    allowed_domains = ["www.formula1.com"]
    start_urls = ["https://www.formula1.com/en.html"]
    
    user_agent_list = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1',
    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18363',
    ]

    def parse(self, response):
        primary_links_list = response.xpath('//*[@id="primaryNav"]/div/div[2]/ul')
        baseurl = "https://www.formula1.com"
        primary_sideurl = []
        for item in primary_links_list:
            link = item.css('li.expandable a::attr(href)').get() 
            primary_sideurl.append(link)
        
        for sideurl in primary_sideurl:
            fullurl = str(baseurl) + str(sideurl)
            yield response.follow(fullurl, callback=self.parse_url, headers={"User-Agent": random.choice(self.user_agent_list)}, dont_filter=True)
    
    
    def parse_url(self, response): 
        fullurl = response.url
        # print (fullurl)
        # print ("Hello World")
        if "/en/latest" in fullurl: 
            yield response.follow(fullurl, callback=self.parse_latest, headers={"User-Agent": random.choice(self.user_agent_list)}, dont_filter=True)
        if "/en/racing" in fullurl: 
            yield response.follow(fullurl, callback=self.parse_racing, headers={"User-Agent" : random.choice(self.user_agent_list)}, dont_filter=True)
        if "/results" in fullurl: 
            yield response.follow(fullurl, callback=self.parse_results, headers={"User-Agent" : random.choice(self.user_agent_list)}, dont_filter=True)
        if "en/drivers" in fullurl: 
            yield response.follow(fullurl, callback=self.parse_drivers, headers={"User-Agent" : random.choice(self.user_agent_list)}, dont_filter=True)
        if "en/teams" in fullurl:
            yield response.follow(fullurl, callback=self.parse_teams, headers={"User-Agent" : random.choice(self.user_agent_list)}, dont_filter=True)        
    
    
    def parse_latest(self, response):
        top_stories = response.xpath('//*[@id="maincontent"]/section[1]/section[2]/fieldset/section')
        top_stories_list = top_stories.css("ul.grid li a div div p ::text").getall()
        top_stories_urls = top_stories.css("ul.grid li a ::attr(href)").getall()
        story_item = Stories()
        
        for i in range(0, len(top_stories_urls)): 
            story_item['story_name'] = top_stories_list[i]
            story_item['story_url'] = top_stories_urls[i]
            yield response.follow(top_stories_urls[i], callback=self.parse_top_news_content, headers={"User-Agent" : random.choice(self.user_agent_list)}, dont_filter=True)
            yield story_item
        
        more_news_section = response.xpath('//*[@id="maincontent"]/section[1]/section[3]/section/div/h2')
        latest_news_url = more_news_section.css('a ::attr(href)').get() 
        yield response.follow(latest_news_url, callback=self.parse_latest_news_content, headers={"User-Agent" : random.choice(self.user_agent_list)}, dont_filter=True)
    
    
    def parse_top_news_content(self, response):
        news_content_structure = response.xpath('//*[@id="maincontent"]/section[2]/section/article/section[1]/div')
        content_list = news_content_structure.css("p ::text").getall() 
        story_item = Stories()
        content_string = ''
        for content in content_list: 
            content_string += content 
        story_item['story_content'] = content_string
        yield story_item
    
    def parse_latest_news_content(self, response):
        # Blocked News Content, we may need to use Selenium Request instead 
        pass
    