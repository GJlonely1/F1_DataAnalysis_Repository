import scrapy
import random 
from time import sleep
from random import randint 
from F1_WebScrape.items import Stories
from scrapy_selenium import SeleniumRequest

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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
        yield SeleniumRequest(url=latest_news_url, callback=self.parse_latest_news, wait_time=10)
    
    
    def parse_top_news_content(self, response):
        news_content_structure = response.xpath('//*[@id="maincontent"]/section[2]/section/article/section[1]/div')
        content_list = news_content_structure.css("p ::text").getall() 
        story_item = Stories()
        content_string = ''
        for content in content_list: 
            content_string += content 
        story_item['story_content'] = content_string
        yield story_item
    
    def parse_latest_news(self, response):
        url = response.url
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        driver.get(url=url)
        sleep(randint(1, 10))

        # Wait for the cookie consent popup and handle it
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="notice"]/div[3]/button[2]'))
            )
            accept_button = driver.find_element(By.XPATH, '//*[@id="notice"]/div[3]/button[2]')
            accept_button.click()
            sleep(randint(1, 10)) # Wait for random seconds to ensure the popup is closed
        except Exception as e:
            self.logger.info(f"No cookie consent popup found: {e}")
        
        
        latest_news = driver.find_elements(By.XPATH, '//*[@id="maincontent"]/div[3]/ul/li')
        for news in latest_news:
            latest_news_item = Stories()
            latest_news_item['story_name'] = news.find_element(By.CSS_SELECTOR, 'a figcaption p').text
            news_url = news.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
            latest_news_item['story_url'] = news_url
            yield latest_news_item
            yield SeleniumRequest(url=news_url, callback=self.parse_latest_news_content)

    
    def parse_latest_news_content(self, response):
        url = response.url
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        driver.get(url=url)
        
                # Wait for the cookie consent popup and handle it
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'button[title="ACCEPT ALL"]'))
            )
            accept_button = driver.find_element(By.CSS_SELECTOR, 'button[title="ACCEPT ALL"]')
            accept_button.click()
            sleep(randint(1, 10)) # Wait for random seconds to ensure the popup is closed
        except Exception as e:
            self.logger.info(f"No cookie consent popup found: {e}")
        
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="maincontent"]/section[2]/section/article'))
            )
            sleep(randint(1, 10)) 
            news_content_elements = driver.find_elements(By.CSS_SELECTOR, 'div p')
            story_item = Stories()
            content_string = ' '.join([element.text for element in news_content_elements])
            story_item['story_content'] = content_string
            yield story_item
        except Exception as e:
            self.logger.info(f"No news content found: {e}")
        
        
    