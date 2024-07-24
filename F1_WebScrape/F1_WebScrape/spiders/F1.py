import scrapy
import random 
from time import sleep
from random import randint 
from F1_WebScrape.items import Stories, RacingSchedule, OverallSingleSeasonRaceResults
from scrapy_selenium import SeleniumRequest

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


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
        primary_links_structure = response.xpath('//*[@id="primaryNav"]/div/div[2]/ul')
        primary_links_list = primary_links_structure.css('ul li.expandable')
        baseurl = "https://www.formula1.com"
        primary_sideurl = []
        for item in primary_links_list:
            link = item.css('a::attr(href)').get() 
            primary_sideurl.append(link)
        
        for sideurl in primary_sideurl:
            fullurl = str(baseurl) + str(sideurl)
            yield response.follow(fullurl, callback=self.parse_url, headers={"User-Agent": random.choice(self.user_agent_list)}, dont_filter=True)
    
    
    def parse_url(self, response): 
        fullurl = response.url
        if "/en/latest" in fullurl: 
            yield response.follow(fullurl, callback=self.parse_latest, headers={"User-Agent": random.choice(self.user_agent_list)}, dont_filter=True)
        elif "/en/racing" in fullurl: 
            yield SeleniumRequest(url=fullurl, callback=self.parse_racing, wait_time=10)
        elif "en/results" in fullurl: 
            yield response.follow(fullurl, callback=self.parse_overall_season_results, headers={"User-Agent" : random.choice(self.user_agent_list)}, dont_filter=True)
        # elif "en/drivers" in fullurl: 
        #     yield response.follow(fullurl, callback=self.parse_drivers, headers={"User-Agent" : random.choice(self.user_agent_list)}, dont_filter=True)
        # elif "en/teams" in fullurl:
        #     yield response.follow(fullurl, callback=self.parse_teams, headers={"User-Agent" : random.choice(self.user_agent_list)}, dont_filter=True)        
    
    
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
        sleep(randint(1, 5))
        # Wait for the cookie consent popup and handle it
        try:
            wait = WebDriverWait(driver, 10)
            accept_element = wait.until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="notice"]/div[3]/button[2]'))
            )
            actions = ActionChains(driver)
            actions.click(accept_element).perform()
            sleep(randint(1, 5)) # Wait for random seconds to ensure the popup is closed
        except Exception as e:
            self.logger.info(f"No cookie consent popup found: {e}")
    
        
        # Scroll and click 'Load More' button
        while True:
            try:
                current_url = driver.current_url
            # Randomly scroll down the page
                scroll_position = random.randint(1000, 2000)  # Random scroll length
                driver.execute_script(f"window.scrollBy(0, {scroll_position});")
                sleep(random.randint(2, 5))  # Wait for the page to load

                # Wait for the 'Load More' button to be visible and clickable
                load_more_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="maincontent"]/section[3]/a')))

                # Check if the 'Load More' button is displayed
                if load_more_button.is_displayed():
                    # Click the 'Load More' button
                    actions = ActionChains(driver)
                    actions.move_to_element(load_more_button).click().perform()
                    self.logger.info("Clicked 'Load More' button")
                    sleep(random.randint(2, 5))  # Wait for more content to load
                    
                    # Wait for the URL to change
                    WebDriverWait(driver, 10).until(lambda d: d.current_url != current_url)
                    self.logger.info(f"URL changed to: {driver.current_url}")
                else:
                    self.logger.info("No more 'Load More' button displayed")
                    break

            except Exception as e:
                self.logger.info(f"No more 'Load More' button found or an error occurred: {e}")
                break
        
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
        # driver = self.setup_driver()
        driver.get(url=url)

        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'button[title="ACCEPT ALL"]'))
            )
            accept_button = driver.find_element(By.CSS_SELECTOR, 'button[title="ACCEPT ALL"]')
            accept_button.click()
            sleep(randint(2, 5)) # Wait for random seconds to ensure the popup is closed
        except Exception as e:
            self.logger.info(f"No cookie consent popup found: {e}")
        
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="maincontent"]/section[2]/section/article'))
            )
            sleep(randint(1, 5)) 
            news_content_elements = driver.find_elements(By.CSS_SELECTOR, 'div p')
            story_item = Stories()
            content_string = ' '.join([element.text for element in news_content_elements])
            story_item['story_content'] = content_string
            yield story_item
        except Exception as e:
            self.logger.info(f"No news content found: {e}")
    
    def parse_racing(self, response):
        current_url = response.url
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        # driver = self.setup_driver()
        driver.get(url=current_url)
        sleep(randint(2,10))
        # Wait for the cookie consent popup and handle it
        try:
            wait = WebDriverWait(driver, 10)
            accept_element = wait.until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="notice"]/div[3]/button[2]'))
            )
            actions = ActionChains(driver)
            actions.click(accept_element).perform()
            sleep(randint(1, 5)) # Wait for random seconds to ensure the popup is closed
        except Exception as e:
            self.logger.info(f"No cookie consent popup found: {e}")
        
        try: 
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="maincontent"]/div/div[1]/div[2]/div/div'))
            )
            racing_structure_list = driver.find_elements(By.CSS_SELECTOR, '.outline-offset-4.outline-metallicBlue.group.outline-0.focus-visible\\:outline-2')
            for indiv_race in racing_structure_list: 
                race_schedule = RacingSchedule()
                race_schedule['race_round'] = indiv_race.find_element(By.CSS_SELECTOR, 'fieldset legend p').text
                # After retrieving race_url, we want to perhaps view the top 3 race winners. I have not figured out the actual use case for the url yet.
                race_schedule['race_url'] = indiv_race.get_attribute('href')  
                race_date_element = indiv_race.find_element(By.CSS_SELECTOR, 'fieldset div div div p span').text + " " + indiv_race.find_element(By.CSS_SELECTOR, 'fieldset div div div.gap-xxs p span').text         
                location_element = indiv_race.find_element(By.CSS_SELECTOR, 'fieldset div div div p.f1-heading').text
                fullname_element = indiv_race.find_element(By.CSS_SELECTOR,'fieldset div div div.min-h-0 p').text
                if location_element and fullname_element and race_date_element is not None: 
                    race_schedule['race_date'] = race_date_element
                    race_schedule['location'] = location_element
                    race_schedule['race_fullname'] = fullname_element
                else: 
                    race_date_element = indiv_race.find_element(By.CSS_SELECTOR, 'fieldset div div div div div div p span').text + " " + indiv_race.find_element(By.CSS_SELECTOR, 'fieldset div div div div div div div span span').text
                    location_element = indiv_race.find_element(By.CSS_SELECTOR, 'fieldset div div div div p').text
                    fullname_element = indiv_race.find_element(By.CSS_SELECTOR, 'fieldset div div div div div p').text
                    race_schedule['race_date'] = race_date_element
                    race_schedule['location'] = location_element
                    race_schedule['race_fullname'] = fullname_element
                yield race_schedule
        except Exception as e:
            self.logger.info(f"No racing info found or an error occurred: {e}")
            
    
    def parse_overall_season_results(self, response): 
        year_elements_structure = response.xpath('/html/body/div[1]/main/article/div/div[2]/div[1]/div[1]/ul')
        # Returns a list of <Selector> e.g. 2024, 2023, 2022, etc. 
        year_elements = year_elements_structure.css("li") 
        
        results_type_structure = response.xpath('/html/body/div[1]/main/article/div/div[2]/div[1]/div[2]/ul')
        # Returns a list of results type <Selector> e.g. Races, Drivers, Teams, DHL Fastest Lap Awards 
        results_type_elements = results_type_structure.css("li")
        
        race_location_structure = response.xpath('/html/body/div[1]/main/article/div/div[2]/div[1]/div[3]/ul')
        # Returns a list of race_locations <Selector> e.g. All, Bahrain, Hungary, etc.
        race_location_elements = race_location_structure.css("li")
        
        base_url = 'https://www.formula1.com/en/results.html'
        # Need to create an f-string that will be iterated over the three variables here. Create a self.parse function 
        
        
        overall_race_results_structure = response.xpath('/html/body/div[1]/main/article/div/div[2]/div[2]/div/div[2]/table/tbody')
        overall_race_results_elements = overall_race_results_structure.css("tr")
        season_results = OverallSingleSeasonRaceResults() 
        season_results['year'] = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[2]/div/div[1]/h1/text()').get()
        for indiv_race_results in overall_race_results_elements: 
            race_fields_unfiltered = indiv_race_results.css("td ::text").getall()
            race_fields_filtered = [field for field in race_fields_unfiltered if field.replace('\n', '').replace(' ', '') != '']
            season_results['grand_prix'] = race_fields_filtered[0]
            season_results['date'] = race_fields_filtered[1]
            season_results['race_winner'] = race_fields_filtered[2] + race_fields_filtered[3] + "," + race_fields_filtered[4]
            season_results['car'] = race_fields_filtered[-3]
            season_results['laps'] = race_fields_filtered[-2]
            season_results['time'] = race_fields_filtered[-1]
            yield season_results                    
                
            
            
            
        