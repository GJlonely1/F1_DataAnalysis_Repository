import os
import scrapy
import random 
import logging 
from time import sleep
from random import randint 
from F1_WebScrape.items import Stories, RacingSchedule, OverallSingleSeasonRaceResults, IndividualRaceResults, IndividualRaceFastestLaps,DriverPitStopSummary, StartingGrid, Qualifying, Practice3, Practice2, Practice1, DriverStandings, ConstructorStandings, DriverRaceStandingsProgression, TeamRaceStandingsProgression, DriverInformation
from scrapy_selenium import SeleniumRequest

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
        # if "/en/latest" in fullurl: 
        #     yield response.follow(fullurl, callback=self.parse_latest, headers={"User-Agent": random.choice(self.user_agent_list)}, dont_filter=True)
        # elif "/en/racing" in fullurl: 
        #     yield SeleniumRequest(url=fullurl, callback=self.parse_racing, wait_time=10)
        if "en/results" in fullurl: 
            yield response.follow(fullurl, callback=self.parse_current_season_results, headers={"User-Agent" : random.choice(self.user_agent_list)}, dont_filter=True)
        elif "en/drivers" in fullurl: 
            yield response.follow(fullurl, callback=self.parse_drivers, headers={"User-Agent" : random.choice(self.user_agent_list)}, dont_filter=True)
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
    #     yield SeleniumRequest(url=latest_news_url, callback=self.parse_latest_news, wait_time=10)
    
    
    # def parse_top_news_content(self, response):
    #     news_content_structure = response.xpath('//*[@id="maincontent"]/section[2]/section/article/section[1]/div')
    #     content_list = news_content_structure.css("p ::text").getall() 
    #     story_item = Stories()
    #     content_string = ''
    #     for content in content_list: 
    #         content_string += content 
    #     story_item['story_content'] = content_string
    #     yield story_item
    
    # def parse_latest_news(self, response):
    #     url = response.url
    #     options = webdriver.ChromeOptions()
    #     options.add_experimental_option('excludeSwitches', ['enable-logging'])
    #     chrome_install = ChromeDriverManager().install()
    #     folder = os.path.dirname(chrome_install)
    #     chromedriver_path = os.path.join(folder, "chromedriver.exe")
    #     driver = webdriver.Chrome(service=ChromeService(chromedriver_path), options=options)
    #     driver.get(url=url)
    #     sleep(randint(1, 5))
    #     # Wait for the cookie consent popup and handle it
    #     try:
    #     # Switch to iframe if necessary
    #         WebDriverWait(driver, 20).until(
    #             EC.presence_of_element_located((By.CSS_SELECTOR, 'iframe'))
    #         )
    #         iframe = driver.find_element(By.CSS_SELECTOR, 'iframe')
    #         driver.switch_to.frame(iframe)

    #         # Wait for the accept button to be clickable
    #         accept_button = WebDriverWait(driver, 20).until(
    #             EC.element_to_be_clickable((By.CSS_SELECTOR, '//button[@title="ACCEPT ALL"]'))
    #         )
    #         accept_button.click()
    #         logger.info("Accepted Cookie Consent Popup")
    #         sleep(randint(3, 8))  # Wait for random seconds to ensure the popup is closed
    #         driver.switch_to.default_content()  # Switch back to the main content

    #     except Exception as e:
    #         self.logger.info(f"No cookie consent popup found or unable to click: {e}")
    #     driver.switch_to.default_content()  
    #     sleep(random.uniform(0,2))

    #     # Scroll and click 'Load More' button
    #     stopScrolling = 0
    #     while True:
    #         try:
    #             stopScrolling += 1
    #             # # Scroll down randomly to load more content
    #             # scroll_position = random.randint(1000, 2000)
    #             driver.execute_script(f"window.scrollBy(0, {50});")
    #             sleep(random.uniform(0,1))
    #             if stopScrolling > 120: 
    #                 break
    #             # Locate the 'Load More' button
    #             load_more_button = WebDriverWait(driver, 20).until(
    #                 EC.presence_of_element_located((By.XPATH, '//*[@id="maincontent"]/section[3]/a'))
    #             )
                
    #             # Click the 'Load More' button if it is displayed
    #             if load_more_button.is_displayed():
    #                 actions = ActionChains(driver)
    #                 actions.move_to_element(load_more_button).click().perform()
    #                 self.logger.info("Clicked 'Load More' button")
    #                 print (driver.page_source)
    #                 sleep(random.randint(3, 5))  # Wait for more content to load
    #             else:
    #                 self.logger.info("No more 'Load More' button displayed")
    #                 break
    #         except Exception as e:
    #             self.logger.info(f"No more 'Load More' button found or an error occurred: {e}")
    #             break
        
    #     latest_news = driver.find_elements(By.XPATH, '//*[@id="maincontent"]/div[3]/ul/li')
    #     for news in latest_news:
    #         latest_news_item = Stories()
    #         latest_news_item['story_name'] = news.find_element(By.CSS_SELECTOR, 'a figcaption p').text
    #         news_url = news.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
    #         latest_news_item['story_url'] = news_url
    #         yield latest_news_item
    #         yield SeleniumRequest(url=news_url, callback=self.parse_latest_news_content)
        

    # def parse_latest_news_content(self, response):
    #     url = response.url
    #     options = webdriver.ChromeOptions()
    #     chrome_install = ChromeDriverManager().install()
    #     folder = os.path.dirname(chrome_install)
    #     chromedriver_path = os.path.join(folder, "chromedriver.exe")
    #     driver = webdriver.Chrome(service=ChromeService(chromedriver_path), options=options)
    #     # driver = self.setup_driver()
    #     driver.get(url=url)

    #     try:
    #     # Switch to iframe if necessary
    #         WebDriverWait(driver, 20).until(
    #             EC.presence_of_element_located((By.CSS_SELECTOR, 'iframe'))
    #         )
    #         iframe = driver.find_element(By.CSS_SELECTOR, 'iframe')
    #         driver.switch_to.frame(iframe)

    #         # Wait for the accept button to be clickable
    #         accept_button = WebDriverWait(driver, 20).until(
    #             EC.element_to_be_clickable((By.CSS_SELECTOR, '//button[@title="ACCEPT ALL"]'))
    #         )
    #         accept_button.click()
    #         logger.info("Accepted Cookie Consent Popup")
    #         sleep(randint(3, 8))  # Wait for random seconds to ensure the popup is closed
    #         driver.switch_to.default_content()  # Switch back to the main content

    #     except Exception as e:
    #         self.logger.info(f"No cookie consent popup found or unable to click: {e}")
        
    #     driver.switch_to.default_content()
    #     sleep(random.uniform(0,1))
        
    #     try:
    #         WebDriverWait(driver, 20).until(
    #             EC.presence_of_element_located((By.XPATH, '//*[@id="maincontent"]/section[3]/section/article'))
    #         )
    #         sleep(randint(1, 5)) 
    #         news_content_elements = driver.find_elements(By.CSS_SELECTOR, 'div p')
    #         story_item = Stories()
    #         content_string = ' '.join([element.text for element in news_content_elements])
    #         story_item['story_content'] = content_string
    #         yield story_item
    #     except Exception as e:
    #         self.logger.info(f"No news content found: {e}")

    # def parse_racing(self, response):
    #     current_url = response.url
    #     options = webdriver.ChromeOptions()
    #     options.add_argument('--no-sandbox')
    #     options.add_argument('--disable-dev-shm-usage')
    #     options.add_argument('--disable-gpu')
    #     # options.add_argument('--headless')  # Run headless for stability in some environments
    #     options = webdriver.ChromeOptions()
    #     chrome_install = ChromeDriverManager().install()
    #     folder = os.path.dirname(chrome_install)
    #     chromedriver_path = os.path.join(folder, "chromedriver.exe")
    #     driver = webdriver.Chrome(service=ChromeService(chromedriver_path), options=options)
    #     driver.get(url=current_url)
    #     sleep(randint(4,8))

    #     # Wait for the cookie consent popup and handle it --
    #     try:
    #     # Switch to iframe if necessary
    #         WebDriverWait(driver, 20).until(
    #             EC.presence_of_element_located((By.CSS_SELECTOR, 'iframe'))
    #         )
    #         iframe = driver.find_element(By.CSS_SELECTOR, 'iframe')
    #         driver.switch_to.frame(iframe)

    #         # Wait for the accept button to be clickable
    #         accept_button = WebDriverWait(driver, 20).until(
    #             EC.element_to_be_clickable((By.CSS_SELECTOR, '//button[@title="ACCEPT ALL"]'))
    #         )
    #         accept_button.click()
    #         logger.info("Accepted Cookie Consent Popup")
    #         sleep(randint(3, 8))  # Wait for random seconds to ensure the popup is closed
    #         driver.switch_to.default_content()  # Switch back to the main content

    #     except Exception as e:
    #         self.logger.info(f"No cookie consent popup found or unable to click: {e}")
    #     driver.switch_to.default_content()
    #     try: 
    #         main_content_visible = WebDriverWait(driver, 10).until(
    #             EC.visibility_of_element_located((By.XPATH, '//*[@id="maincontent"]/div/div[1]/div[2]/div/div'))
    #         )
    #         sleep(randint(2,5))
    #         main_content_present = WebDriverWait(driver, 10).until(
    #             EC.presence_of_element_located((By.XPATH, '//*[@id="maincontent"]/div/div[1]/div[2]/div/div'))
    #         )

    #         racing_structure_list = driver.find_elements(By.CSS_SELECTOR, '.outline-offset-4.outline-scienceBlue.group.outline-0.focus-visible\\:outline-2')
    #         for indiv_race in racing_structure_list: 
    #             race_schedule = RacingSchedule()
    #             race_schedule['race_round'] = indiv_race.find_element(By.CSS_SELECTOR, 'fieldset legend p').text
    #             # After retrieving race_url, we want to perhaps view the top 3 race winners. I have not figured out the actual use case for the url yet.
    #             race_schedule['race_url'] = indiv_race.get_attribute('href')

    #             race_date_element = indiv_race.find_element(By.CSS_SELECTOR, 'fieldset div div div p span').text + " " + indiv_race.find_element(By.CSS_SELECTOR, 'fieldset div div div.gap-xxs p span').text         
    #             location_element = indiv_race.find_element(By.CSS_SELECTOR, 'fieldset div div div p.f1-heading').text
    #             fullname_element = indiv_race.find_element(By.CSS_SELECTOR,'fieldset div div div.min-h-0 p').text
    #             if location_element and fullname_element and race_date_element: 
    #                 race_schedule['race_date'] = race_date_element
    #                 race_schedule['location'] = location_element
    #                 race_schedule['race_fullname'] = fullname_element
    #             else: 
    #                 race_date_element = indiv_race.find_element(By.CSS_SELECTOR, 'fieldset div div div div div div p span').text + " " + indiv_race.find_element(By.CSS_SELECTOR, 'fieldset div div div div div div div span span').text
    #                 location_element = indiv_race.find_element(By.CSS_SELECTOR, 'fieldset div div div div p').text
    #                 fullname_element = indiv_race.find_element(By.CSS_SELECTOR, 'fieldset div div div div div p').text
    #                 race_schedule['race_date'] = race_date_element
    #                 race_schedule['location'] = location_element
    #                 race_schedule['race_fullname'] = fullname_element
    #             yield race_schedule
    #     except Exception as e:
    #         self.logger.info(f"No racing info found or an error occurred: {e}")
    #     finally:
    #         driver.quit()
            
    
    def parse_current_season_results(self, response):         
        base_url = 'https://www.formula1.com'
        year_elements_structure = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[1]/details[1]/div/ul')
        # Returns a list of Years <Selector> e.g. 2024, 2023, 2022, etc. 
        year_elements = year_elements_structure.css("li") 
        years_sideurl_list = year_elements.css("a ::attr(href)").getall()
        # years_text_list = year_elements.css("a ::text").getall()
        for indiv_sideurl in years_sideurl_list[1:]:
            official_year_season_results_url = str(base_url) + str(indiv_sideurl)
            yield response.follow(official_year_season_results_url, callback=self.parse_past_season_results, headers={"User-Agent" : random.choice(self.user_agent_list)}, dont_filter=True)
        
        # this only applies to 2024, the structure is different for each year. 
        results_type_structure = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[1]/details[2]/div/ul')
        # Returns a list of results type <Selector> e.g. Races, Drivers, Teams, DHL Fastest Lap Awards 
        results_type_elements = results_type_structure.css("li")
        for indiv_type in results_type_elements[1:]: 
            categories_sideurl = indiv_type.css("a ::attr(href)").get() 
            official_category_url = base_url + categories_sideurl
            if '/drivers' in official_category_url: 
                yield response.follow(official_category_url, callback=self.parse_current_season_driver_standings, headers={"User-Agent" : random.choice(self.user_agent_list)}, dont_filter=True)
            elif '/team' in official_category_url: 
                yield response.follow(official_category_url, callback=self.parse_current_season_team_standings, headers={"User-Agent" : random.choice(self.user_agent_list)}, dont_filter=True)
            # elif '/fastest-laps' in official_category_url:
            #     yield response.follow(official_category_url, callback=self.parse_current_season_fastest_laps, headers={"User-Agent" : random.choice(self.user_agent_list)}, dont_filter=True)
        
        race_location_structure = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[1]/details[3]/div/ul')
        # Returns a list of race_locations <Selector> e.g. All, Bahrain, Hungary, etc.
        race_location_sideurl_list = race_location_structure.css("li a::attr(href)").getall()
        for indiv_location in race_location_sideurl_list[1:]: 
            official_race_location_url = str(base_url) + str(indiv_location)
            yield response.follow(official_race_location_url, callback=self.parse_current_season_individual_race_result, headers={"User-Agent" : random.choice(self.user_agent_list)}, dont_filter=True)
    
        # Need to create an f-string that will be iterated over the three variables here. Create a self.parse function 
        overall_race_results_structure = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[2]/div/div[2]/table/tbody')
        overall_race_results_elements = overall_race_results_structure.css("tr")
        season_results = OverallSingleSeasonRaceResults() 
        season_results['year'] = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[2]/div/div[1]/h1/text()').get()
        for indiv_race_results in overall_race_results_elements: 
            race_fields_unfiltered = indiv_race_results.css("td ::text").getall()
            race_fields_filtered = [field for field in race_fields_unfiltered if field.replace('\n', '').replace(' ', '') != '']
            season_results['grand_prix'] = race_fields_filtered[0]
            season_results['date'] = race_fields_filtered[1]
            season_results['race_winner'] = f"{race_fields_filtered[2]} {race_fields_filtered[4]}"
            season_results['car'] = race_fields_filtered[-3]
            season_results['laps'] = race_fields_filtered[-2]
            season_results['time'] = race_fields_filtered[-1]
            yield season_results          
        # sleep(randint(1,2))          
    
    # Logic: In each year, the race locations may not be the same. I initially thought retrieving race_locations from 2024 and fixing the years will result in responses.
    # Redirection successful, but we need to account for varying years and varying locations hence urls will be different. Need to vary that. 

    def parse_past_season_results(self, response): 
        base_url = 'https://www.formula1.com'
        # e.g. "https://www.formula1.com/en/results/2024/races", "https://www.formula1.com/en/results/2023/races"
        overall_race_results_structure = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[2]/div/div[2]/table/tbody')
        overall_race_results_elements = overall_race_results_structure.css("tr")
        season_results = OverallSingleSeasonRaceResults() 
        season_results['year'] = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[2]/div/div[1]/h1/text()').get()
        for indiv_race_results in overall_race_results_elements: 
            race_fields_unfiltered = indiv_race_results.css("td ::text").getall()
            race_fields_filtered = [field for field in race_fields_unfiltered if field.replace('\n', '').replace(' ', '') != '']
            season_results['grand_prix'] = race_fields_filtered[0]
            season_results['date'] = race_fields_filtered[1]
            season_results['race_winner'] = race_fields_filtered[2] + ' ' + race_fields_filtered[4]
            season_results['car'] = race_fields_filtered[-3]
            season_results['laps'] = race_fields_filtered[-2]
            season_results['time'] = race_fields_filtered[-1]
            yield season_results
        # sleep(random.uniform(0, 1))
        
        race_location_structure = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[1]/details[3]/div/ul')
        race_location_sideurl_list = race_location_structure.css("li a::attr(href)").getall()
        for indiv_location_url in race_location_sideurl_list[1:]:
            official_race_location_url = f"{base_url}{indiv_location_url}"
            yield response.follow(official_race_location_url, callback=self.past_seasons_individual_race_results,headers={"User-Agent" : random.choice(self.user_agent_list)}, dont_filter=True)

        race_categories_structure = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[1]/details[2]/div/ul')
        race_categories_elements = race_categories_structure.css("li")
        for indiv_category_elem in race_categories_elements[1:]:
            indiv_category_sideurl = indiv_category_elem.css("a ::attr(href)").get()
            official_race_category_url = f"{base_url}{indiv_category_sideurl}"
            if '/drivers' in official_race_category_url: 
                yield response.follow(official_race_category_url, callback=self.parse_past_seasons_driver_standings, headers={"User-Agent" : random.choice(self.user_agent_list)}, dont_filter=True)
            elif '/team' in official_race_category_url: 
                yield response.follow(official_race_category_url, callback=self.parse_past_seasons_team_standings, headers={"User-Agent" : random.choice(self.user_agent_list)}, dont_filter=True)
            # elif '/fastest-laps' in official_category_url:
            #     yield response.follow(official_category_url, callback=self.parse_past_seasons_fastest_laps, headers={"User-Agent" : random.choice(self.user_agent_list)}, dont_filter=True)
        
        
    def parse_current_season_individual_race_result(self, response): 
        race_results_structure = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[2]/div/div[3]/div[2]/table/tbody')
        race_results_element = race_results_structure.css("tr")

        # Retrieve the different race_types_urls e.g. race-result, fastest-laps, pit-stop summary etc. 
        race_types_structure = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[2]/div/div[3]/div[1]/ul')
        race_types_sideurl_list = race_types_structure.css("li a ::attr(href)").getall()
        base_url = 'https://www.formula1.com'

        for race_type_url in race_types_sideurl_list[1:]: 
            race_category_fullurl = f"{base_url}{race_type_url}"
            if "fastest-laps" in race_category_fullurl:
                yield response.follow(race_category_fullurl, callback=self.parse_current_season_fastest_laps, headers={"User-Agent" : random.choice(self.user_agent_list)}, dont_filter=True) 
            elif "pit-stop-summary" in race_category_fullurl: 
                yield response.follow(race_category_fullurl, callback=self.parse_current_season_pitstop_summary, headers={"User-Agent" : random.choice(self.user_agent_list)}, dont_filter=True)
            elif "starting-grid" in race_category_fullurl: 
                yield response.follow(race_category_fullurl, callback=self.parse_current_season_starting_grid, headers={"User-Agent" : random.choice(self.user_agent_list)}, dont_filter=True)
            elif "qualifying" in race_category_fullurl:
                yield response.follow(race_category_fullurl, callback=self.parse_current_season_qualifying_results, headers={"User-Agent" : random.choice(self.user_agent_list)}, dont_filter=True)
            elif "practice/3" in race_category_fullurl:
                yield response.follow(race_category_fullurl, callback=self.parse_current_season_practice3_results,headers={"User-Agent" : random.choice(self.user_agent_list)}, dont_filter=True)
            elif "practice/2" in race_category_fullurl:
                yield response.follow(race_category_fullurl, callback=self.parse_current_season_practice2_results,headers={"User-Agent" : random.choice(self.user_agent_list)}, dont_filter=True)
            elif "practice/1" in race_category_fullurl:
                yield response.follow(race_category_fullurl, callback=self.parse_current_season_practice1_results,headers={"User-Agent" : random.choice(self.user_agent_list)}, dont_filter=True)
                
        race_results = IndividualRaceResults()
        race_results['year'] = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[2]/div/div[2]/p[1]/text()').get()[-4:]
        race_results['race_fullname'] = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[2]/div/div[1]/h1/text()').get()
        race_results['race_date'] = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[2]/div/div[2]/p[1]/text()').get()
        race_results['race_circuit'] = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[2]/div/div[2]/p[2]/text()').get()
        for indiv_position in race_results_element: 
            stats_unfiltered_list = indiv_position.css("td ::text").getall() 
            stats_filtered_list =[elem for elem in stats_unfiltered_list if elem != '\xa0']
            race_results['position'] = stats_filtered_list[0]
            race_results['car_number'] = stats_filtered_list[1]
            race_results['driver'] = stats_filtered_list[2] + ' ' + stats_filtered_list[3]
            race_results['car'] = stats_filtered_list[-4]
            race_results['laps'] = stats_filtered_list[-3]
            race_results['time_or_retired'] = stats_filtered_list[-2]
            race_results['points'] = stats_filtered_list[-1]
            yield race_results
        # sleep(randint(1,2))
    
    def past_seasons_individual_race_results(self, response): 
        race_results_structure = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[2]/div/div[3]/div[2]/table/tbody')
        race_results_element = race_results_structure.css("tr")

        race_results = IndividualRaceResults()
        race_results['year'] = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[2]/div/div[2]/p[1]/text()').get()[-4:]
        race_results['race_fullname'] = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[2]/div/div[1]/h1/text()').get()
        race_results['race_date'] = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[2]/div/div[2]/p[1]/text()').get()
        race_results['race_circuit'] = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[2]/div/div[2]/p[2]/text()').get()
        for indiv_position in race_results_element: 
            stats_unfiltered_list = indiv_position.css("td ::text").getall() 
            stats_filtered_list =[elem for elem in stats_unfiltered_list if elem != '\xa0']
            race_results['position'] = stats_filtered_list[0]
            race_results['car_number'] = stats_filtered_list[1]
            race_results['driver'] = stats_filtered_list[2] + ' ' + stats_filtered_list[3]
            race_results['car'] = stats_filtered_list[-4]
            race_results['laps'] = stats_filtered_list[-3]
            race_results['time_or_retired'] = stats_filtered_list[-2]
            race_results['points'] = stats_filtered_list[-1]
            yield race_results
        # sleep(random.uniform(0, 1))

        race_types_structure = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[2]/div/div[3]/div[1]/ul')
        race_types_sideurl_list = race_types_structure.css("li a ::attr(href)").getall()
        base_url = 'https://www.formula1.com'
        
        for race_type_url in race_types_sideurl_list[1:]: 
            race_category_fullurl = f"{base_url}{race_type_url}"
            if "fastest-laps" in race_category_fullurl:
                yield response.follow(race_category_fullurl, callback=self.parse_past_seasons_fastest_laps, headers={"User-Agent" : random.choice(self.user_agent_list)}, dont_filter=True) 
            elif "pit-stop-summary" in race_category_fullurl: 
                yield response.follow(race_category_fullurl, callback=self.parse_past_seasons_pitstop_summary, headers={"User-Agent" : random.choice(self.user_agent_list)}, dont_filter=True)
            elif "starting-grid" in race_category_fullurl: 
                yield response.follow(race_category_fullurl, callback=self.parse_past_seasons_starting_grid, headers={"User-Agent" : random.choice(self.user_agent_list)}, dont_filter=True)
            elif "qualifying" in race_category_fullurl:
                yield response.follow(race_category_fullurl, callback=self.parse_past_seasons_qualifying_results, headers={"User-Agent" : random.choice(self.user_agent_list)}, dont_filter=True)
            elif "practice/3" in race_category_fullurl:
                yield response.follow(race_category_fullurl, callback=self.parse_past_seasons_practice3_results,headers={"User-Agent" : random.choice(self.user_agent_list)}, dont_filter=True)
            elif "practice/2" in race_category_fullurl:
                yield response.follow(race_category_fullurl, callback=self.parse_past_seasons_practice2_results,headers={"User-Agent" : random.choice(self.user_agent_list)}, dont_filter=True)
            elif "practice/1" in race_category_fullurl:
                yield response.follow(race_category_fullurl, callback=self.parse_past_seasons_practice1_results,headers={"User-Agent" : random.choice(self.user_agent_list)}, dont_filter=True)
    
    def parse_current_season_fastest_laps(self, response): 
        fastest_laps_structure = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[2]/div/div[3]/div[2]/table/tbody')
        fastest_laps_element = fastest_laps_structure.css("tr")

        fastest_lap_results = IndividualRaceFastestLaps()
        fastest_lap_results['year'] = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[2]/div/div[2]/p[1]/text()').get()[-4:]
        fastest_lap_results['race_fullname'] = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[2]/div/div[1]/h1/text()').get()
        fastest_lap_results['race_date'] = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[2]/div/div[2]/p[1]/text()').get()
        fastest_lap_results['race_circuit'] = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[2]/div/div[2]/p[2]/text()').get()

        for indiv_driver_row in fastest_laps_element: 
            stats_unfiltered_list = indiv_driver_row.css("td ::text").getall()
            stats_filtered_list = [elem for elem in stats_unfiltered_list if elem != '\xa0']
            fastest_lap_results['position'] = stats_filtered_list[0]
            fastest_lap_results['car_number'] = stats_filtered_list[1]
            fastest_lap_results['driver'] = stats_filtered_list[2] + " " + stats_filtered_list[3]
            fastest_lap_results['car'] = stats_filtered_list[5]
            if len(stats_filtered_list) == 10: 
                fastest_lap_results['fastest_lap_number'] = stats_filtered_list[-4]
                fastest_lap_results['time_of_day'] = stats_filtered_list[-3]
                fastest_lap_results['fastest_time'] = stats_filtered_list[-2]
                fastest_lap_results['average_speed'] = stats_filtered_list[-1]
            elif len(stats_filtered_list) == 9: 
                fastest_lap_results['fastest_lap_number'] = stats_filtered_list[-3]
                fastest_lap_results['time_of_day'] = None
                fastest_lap_results['fastest_time'] = stats_filtered_list[-2]
                fastest_lap_results['average_speed'] = stats_filtered_list[-1]
            yield fastest_lap_results
        # sleep(random.uniform(0, 1))
    
    def parse_past_seasons_fastest_laps (self, response): 
        fastest_laps_structure = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[2]/div/div[3]/div[2]/table/tbody')
        fastest_laps_element = fastest_laps_structure.css("tr")

        fastest_lap_results = IndividualRaceFastestLaps()
        fastest_lap_results['year'] = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[2]/div/div[2]/p[1]/text()').get()[-4:]
        fastest_lap_results['race_fullname'] = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[2]/div/div[1]/h1/text()').get()
        fastest_lap_results['race_date'] = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[2]/div/div[2]/p[1]/text()').get()
        fastest_lap_results['race_circuit'] = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[2]/div/div[2]/p[2]/text()').get()

        for indiv_driver_row in fastest_laps_element: 
            stats_unfiltered_list = indiv_driver_row.css("td ::text").getall()
            stats_filtered_list = [elem for elem in stats_unfiltered_list if elem != '\xa0']
            fastest_lap_results['position'] = stats_filtered_list[0]
            fastest_lap_results['car_number'] = stats_filtered_list[1]
            fastest_lap_results['driver'] = stats_filtered_list[2] + " " + stats_filtered_list[3]
            fastest_lap_results['car'] = stats_filtered_list[5]
            if len(stats_filtered_list) == 10: 
                fastest_lap_results['fastest_lap_number'] = stats_filtered_list[-4]
                fastest_lap_results['time_of_day'] = stats_filtered_list[-3]
                fastest_lap_results['fastest_time'] = stats_filtered_list[-2]
                fastest_lap_results['average_speed'] = stats_filtered_list[-1]
            elif len(stats_filtered_list) == 9: 
                fastest_lap_results['fastest_lap_number'] = stats_filtered_list[-3]
                fastest_lap_results['time_of_day'] = None
                fastest_lap_results['fastest_time'] = stats_filtered_list[-2]
                fastest_lap_results['average_speed'] = stats_filtered_list[-1]
            yield fastest_lap_results
        # sleep(random.uniform(0, 1))
    
    def parse_current_season_pitstop_summary (self, response): 
        pit_stop_summary_structure = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[2]/div/div[3]/div[2]/table/tbody')
        pit_stop_summary_elements = pit_stop_summary_structure.css("tr")
        
        driver_pitstop_summary = DriverPitStopSummary() 
        driver_pitstop_summary['year'] = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[2]/div/div[2]/p[1]/text()').get()[-4:]
        driver_pitstop_summary['race_fullname'] = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[2]/div/div[1]/h1/text()').get()
        driver_pitstop_summary['race_date'] = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[2]/div/div[2]/p[1]/text()').get()
        driver_pitstop_summary['race_circuit'] = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[2]/div/div[2]/p[2]/text()').get()
    
        for indiv_driver_row in pit_stop_summary_elements:
            stats_unfiltered_list = indiv_driver_row.css("td ::text").getall()
            stats_filtered_list = [elem for elem in stats_unfiltered_list if elem != '\xa0']
            driver_pitstop_summary['pitstop_count'] = stats_filtered_list[0]
            driver_pitstop_summary['car_number'] = stats_filtered_list[1]
            driver_pitstop_summary['driver'] = stats_filtered_list[2] + " " + stats_filtered_list[3]
            driver_pitstop_summary['car'] = stats_filtered_list[-5]
            driver_pitstop_summary['pit_stop_lap_number'] = stats_filtered_list[-4]
            driver_pitstop_summary['time_of_day_for_pitstop'] = stats_filtered_list[-3]
            driver_pitstop_summary['pit_stop_duration'] = stats_filtered_list[-2]
            driver_pitstop_summary['total_pitstop_duration'] = stats_filtered_list[-1]
            yield driver_pitstop_summary
    
    def parse_past_seasons_pitstop_summary (self, response): 
        pit_stop_summary_structure = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[2]/div/div[3]/div[2]/table/tbody')
        pit_stop_summary_elements = pit_stop_summary_structure.css("tr")
        
        driver_pitstop_summary = DriverPitStopSummary() 
        driver_pitstop_summary['year'] = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[2]/div/div[2]/p[1]/text()').get()[-4:]
        driver_pitstop_summary['race_fullname'] = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[2]/div/div[1]/h1/text()').get()
        driver_pitstop_summary['race_date'] = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[2]/div/div[2]/p[1]/text()').get()
        driver_pitstop_summary['race_circuit'] = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[2]/div/div[2]/p[2]/text()').get()

        for indiv_driver_row in pit_stop_summary_elements:
            stats_unfiltered_list = indiv_driver_row.css("td ::text").getall()
            stats_filtered_list = [elem for elem in stats_unfiltered_list if elem != '\xa0']
            driver_pitstop_summary['pitstop_count'] = stats_filtered_list[0]
            driver_pitstop_summary['car_number'] = stats_filtered_list[1]
            driver_pitstop_summary['driver'] = stats_filtered_list[2] + " " + stats_filtered_list[3]
            driver_pitstop_summary['car'] = stats_filtered_list[-5]
            driver_pitstop_summary['pit_stop_lap_number'] = stats_filtered_list[-4]
            driver_pitstop_summary['time_of_day_for_pitstop'] = stats_filtered_list[-3]
            driver_pitstop_summary['pit_stop_duration'] = stats_filtered_list[-2]
            driver_pitstop_summary['total_pitstop_duration'] = stats_filtered_list[-1]
            yield driver_pitstop_summary
        # sleep(random.uniform(0, 1))
    
    def parse_current_season_starting_grid(self, response): 
        starting_grid_structure = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[2]/div/div[3]/div[2]/table/tbody')
        starting_grid_elements = starting_grid_structure.css("tr")
        
        starting_grid = StartingGrid()
        starting_grid['year'] = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[2]/div/div[2]/p[1]/text()').get()[-4:]
        starting_grid['race_fullname'] = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[2]/div/div[1]/h1/text()').get()
        starting_grid['race_date'] = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[2]/div/div[2]/p[1]/text()').get()
        starting_grid['race_circuit'] = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[2]/div/div[2]/p[2]/text()').get()
        
        for indiv_driver_row in starting_grid_elements:
            stats_unfiltered_list = indiv_driver_row.css("td ::text").getall()
            stats_filtered_list = [elem for elem in stats_unfiltered_list if elem != '\xa0']
            starting_grid['position'] = stats_filtered_list[0]
            starting_grid['car_number'] = stats_filtered_list[1]
            starting_grid['driver'] = stats_filtered_list[2] + " " + stats_filtered_list[3]
            if len(stats_filtered_list) == 7:
                starting_grid['car'] = stats_filtered_list[-2]
                starting_grid['qualifying_time'] = stats_filtered_list[-1]
            elif len(stats_filtered_list) == 6: 
                starting_grid['car'] = stats_filtered_list[-1]
                starting_grid['qualifying_time'] = None
            yield starting_grid
    
    def parse_past_seasons_starting_grid (self, response): 
        starting_grid_structure = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[2]/div/div[3]/div[2]/table/tbody')
        starting_grid_elements = starting_grid_structure.css("tr")
        
        starting_grid = StartingGrid()
        starting_grid['year'] = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[2]/div/div[2]/p[1]/text()').get()[-4:]
        starting_grid['race_fullname'] = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[2]/div/div[1]/h1/text()').get()
        starting_grid['race_date'] = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[2]/div/div[2]/p[1]/text()').get()
        starting_grid['race_circuit'] = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[2]/div/div[2]/p[2]/text()').get()
        
        for indiv_driver_row in starting_grid_elements:
            stats_unfiltered_list = indiv_driver_row.css("td ::text").getall()
            stats_filtered_list = [elem for elem in stats_unfiltered_list if elem != '\xa0']
            starting_grid['position'] = stats_filtered_list[0]
            starting_grid['car_number'] = stats_filtered_list[1]
            starting_grid['driver'] = stats_filtered_list[2] + " " + stats_filtered_list[3]
            starting_grid['car'] = stats_filtered_list[-2]
            starting_grid['qualifying_time'] = stats_filtered_list[-1]
            yield starting_grid
        # sleep(random.uniform(0, 1))
    
    def parse_current_season_qualifying_results (self, response): 
        qualifying_structure = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[2]/div/div[3]/div[2]/table/tbody')
        qualifying_elements = qualifying_structure.css("tr")

        qualification_results = Qualifying()
        qualification_results['year'] = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[2]/div/div[2]/p[1]/text()').get()[-4:]
        qualification_results['race_fullname'] = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[2]/div/div[1]/h1/text()').get()
        qualification_results['race_date'] = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[2]/div/div[2]/p[1]/text()').get()
        qualification_results['race_circuit'] = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[2]/div/div[2]/p[2]/text()').get()
        
        for indiv_driver_row in qualifying_elements:
            stats_unfiltered_list = indiv_driver_row.css("td ::text").getall()
            stats_filtered_list = [elem for elem in stats_unfiltered_list if elem != '\xa0']
            qualification_results['position'] = stats_filtered_list[0]
            qualification_results['car_number'] = stats_filtered_list[1]
            qualification_results['driver'] = stats_filtered_list[2] + " " + stats_filtered_list[3]
            qualification_results['car'] = stats_filtered_list[5]
            qualification_results['total_laps_completed'] = stats_filtered_list[-1]
            
            if len(stats_filtered_list) == 8: 
                qualification_results['Q1_time'] = stats_filtered_list[-2]
                qualification_results['Q2_time'] = None
                qualification_results['Q3_time'] = None
                qualification_results['Final_Qualifying_time'] = stats_filtered_list[-2]
            elif len(stats_filtered_list) == 9: 
                qualification_results['Q1_time'] = stats_filtered_list[-3]
                qualification_results['Q2_time'] = stats_filtered_list[-2]
                qualification_results['Q3_time'] = None
                qualification_results['Final_Qualifying_time'] = stats_filtered_list[-2]
            elif len(stats_filtered_list) == 10:
                qualification_results['Q1_time'] = stats_filtered_list[-4]
                qualification_results['Q2_time'] = stats_filtered_list[-3]
                qualification_results['Q3_time'] = stats_filtered_list[-2]
                qualification_results['Final_Qualifying_time'] = stats_filtered_list[-2]
            yield qualification_results
    
    # Current Logic only checks for "qualifying", does not check for "qualifying/0", "qualifying/1", etc. from older seasons hence all data points may appear duplicated, unless we do a check in this function for the explicit qualifying
    def parse_past_seasons_qualifying_results (self, response): 
        qualifying_structure = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[2]/div/div[3]/div[2]/table/tbody')
        qualifying_elements = qualifying_structure.css("tr")

        qualification_results = Qualifying()
        qualification_results['year'] = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[2]/div/div[2]/p[1]/text()').get()[-4:]
        qualification_results['race_fullname'] = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[2]/div/div[1]/h1/text()').get()
        qualification_results['race_date'] = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[2]/div/div[2]/p[1]/text()').get()
        qualification_results['race_circuit'] = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[2]/div/div[2]/p[2]/text()').get()
        
        for indiv_driver_row in qualifying_elements:
            stats_unfiltered_list = indiv_driver_row.css("td ::text").getall() 
            stats_filtered_list = [elem for elem in stats_unfiltered_list if elem != '\xa0']
            qualification_results['position'] = stats_filtered_list[0]
            qualification_results['car_number'] = stats_filtered_list[1]
            qualification_results['driver'] = stats_filtered_list[2] + " " + stats_filtered_list[3]
            qualification_results['car'] = stats_filtered_list[5]
            
            if len(stats_filtered_list) == 7:
                qualification_results['Q1_time'] = None
                qualification_results['Q2_time'] = None
                qualification_results['Q3_time'] = stats_filtered_list[-1]
                qualification_results['Final_Qualifying_time'] = stats_filtered_list[-1]
            elif (len(stats_filtered_list) == 8): 
                qualification_results['Q1_time'] = stats_filtered_list[-2]
                qualification_results['Q2_time'] = None
                qualification_results['Q3_time'] = None
                qualification_results['Final_Qualifying_time'] = stats_filtered_list[-2]
                qualification_results['total_laps_completed'] = stats_filtered_list[-1]
            elif len(stats_filtered_list) == 9:
                qualification_results['Q1_time'] = stats_filtered_list[-3]
                qualification_results['Q2_time'] = stats_filtered_list[-2]
                qualification_results['Q3_time'] = None
                qualification_results['Final_Qualifying_time'] = stats_filtered_list[-2]
                qualification_results['total_laps_completed'] = stats_filtered_list[-1]
            elif len(stats_filtered_list) == 10: 
                qualification_results['Q1_time'] = stats_filtered_list[-4]
                qualification_results['Q2_time'] = stats_filtered_list[-3]
                qualification_results['Q3_time'] = stats_filtered_list[-2]
                qualification_results['Final_Qualifying_time'] = stats_filtered_list[-2]
                qualification_results['total_laps_completed'] = stats_filtered_list[-1]    
            
            yield qualification_results
        # sleep(random.uniform(0, 1))
    
    def parse_current_season_practice3_results (self, response): 
        practice3_structure = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[2]/div/div[3]/div[2]/table/tbody')
        practice3_elements = practice3_structure.css("tr")
        
        practice3_results = Practice3()
        practice3_results['year'] = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[2]/div/div[2]/p[1]/text()').get()[-4:]
        practice3_results['race_fullname'] = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[2]/div/div[1]/h1/text()').get()
        practice3_results['race_date'] = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[2]/div/div[2]/p[1]/text()').get()
        practice3_results['race_circuit'] = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[2]/div/div[2]/p[2]/text()').get()
        
        for indiv_driver_row in practice3_elements: 
            stats_unfiltered_list = indiv_driver_row.css("td ::text").getall()
            stats_filtered_list = [elem for elem in stats_unfiltered_list if elem != '\xa0']
            practice3_results['position'] = stats_filtered_list[0]
            practice3_results['car_number'] = stats_filtered_list[1]
            practice3_results['driver'] = stats_filtered_list[2] + " " + stats_filtered_list[3]

            if len(stats_filtered_list) == 8:
                practice3_results['car'] = stats_filtered_list[-3]
                practice3_results['fastest_time'] = stats_filtered_list[-2] 
                practice3_results['gap_from_1stPosition'] = 0
                practice3_results['total_laps_completed'] = stats_filtered_list[-1]
            elif len(stats_filtered_list) == 9: 
                practice3_results['car'] = stats_filtered_list[-4]
                practice3_results['fastest_time'] = stats_filtered_list[-3] 
                practice3_results['gap_from_1stPosition'] = stats_filtered_list[-2]
                practice3_results['total_laps_completed'] = stats_filtered_list[-1]
                
            yield practice3_results
            
    def parse_past_seasons_practice3_results(self, response): 
        practice3_structure = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[2]/div/div[3]/div[2]/table/tbody')
        practice3_elements = practice3_structure.css("tr")
        
        practice3_results = Practice3()
        practice3_results['year'] = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[2]/div/div[2]/p[1]/text()').get()[-4:]
        practice3_results['race_fullname'] = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[2]/div/div[1]/h1/text()').get()
        practice3_results['race_date'] = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[2]/div/div[2]/p[1]/text()').get()
        practice3_results['race_circuit'] = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[2]/div/div[2]/p[2]/text()').get()
        
        for indiv_driver_row in practice3_elements: 
            stats_unfiltered_list = indiv_driver_row.css("td ::text").getall()
            stats_filtered_list = [elem for elem in stats_unfiltered_list if elem != '\xa0']
            practice3_results['position'] = stats_filtered_list[0]
            practice3_results['car_number'] = stats_filtered_list[1]
            practice3_results['driver'] = stats_filtered_list[2] + " " + stats_filtered_list[3]
            if len(stats_filtered_list) == 8:
                practice3_results['car'] = stats_filtered_list[-3]
                practice3_results['fastest_time'] = stats_filtered_list[-2] 
                practice3_results['gap_from_1stPosition'] = 0
                practice3_results['total_laps_completed'] = stats_filtered_list[-1]
            elif len(stats_filtered_list) == 9: 
                practice3_results['car'] = stats_filtered_list[-4]
                practice3_results['fastest_time'] = stats_filtered_list[-3] 
                practice3_results['gap_from_1stPosition'] = stats_filtered_list[-2]
                practice3_results['total_laps_completed'] = stats_filtered_list[-1]
            yield practice3_results
        # sleep(random.uniform(0, 1))
        
    def parse_current_season_practice2_results (self, response): 
        practice2_structure = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[2]/div/div[3]/div[2]/table/tbody')
        practice2_elements = practice2_structure.css('tr')
        
        practice2_results = Practice2()
        practice2_results['year'] = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[2]/div/div[2]/p[1]/text()').get()[-4:]
        practice2_results['race_fullname'] = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[2]/div/div[1]/h1/text()').get()
        practice2_results['race_date'] = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[2]/div/div[2]/p[1]/text()').get()
        practice2_results['race_circuit'] = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[2]/div/div[2]/p[2]/text()').get()
        
        for indiv_driver_row in practice2_elements: 
            stats_unfiltered_list = indiv_driver_row.css("td ::text").getall()
            stats_filtered_list = [elem for elem in stats_unfiltered_list if elem != '\xa0']
            practice2_results['position'] = stats_filtered_list[0]
            practice2_results['car_number'] = stats_filtered_list[1]
            practice2_results['driver'] = stats_filtered_list[2] + " " + stats_filtered_list[3]
            if len(stats_filtered_list) == 8:
                practice2_results['car'] = stats_filtered_list[-3]
                practice2_results['fastest_time'] = stats_filtered_list[-2] 
                practice2_results['gap_from_1stPosition'] = 0
                practice2_results['total_laps_completed'] = stats_filtered_list[-1]
            elif len(stats_filtered_list) == 9: 
                practice2_results['car'] = stats_filtered_list[-4]
                practice2_results['fastest_time'] = stats_filtered_list[-3] 
                practice2_results['gap_from_1stPosition'] = stats_filtered_list[-2]
                practice2_results['total_laps_completed'] = stats_filtered_list[-1]
                
            yield practice2_results
            
    def parse_past_seasons_practice2_results (self, response): 
        practice2_structure = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[2]/div/div[3]/div[2]/table/tbody')
        practice2_elements = practice2_structure.css('tr')
        
        practice2_results = Practice2()
        practice2_results['year'] = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[2]/div/div[2]/p[1]/text()').get()[-4:]
        practice2_results['race_fullname'] = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[2]/div/div[1]/h1/text()').get()
        practice2_results['race_date'] = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[2]/div/div[2]/p[1]/text()').get()
        practice2_results['race_circuit'] = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[2]/div/div[2]/p[2]/text()').get()
        
        for indiv_driver_row in practice2_elements: 
            stats_unfiltered_list = indiv_driver_row.css("td ::text").getall()
            stats_filtered_list = [elem for elem in stats_unfiltered_list if elem != '\xa0']
            practice2_results['position'] = stats_filtered_list[0]
            practice2_results['car_number'] = stats_filtered_list[1]
            practice2_results['driver'] = stats_filtered_list[2] + " " + stats_filtered_list[3]
            if len(stats_filtered_list) == 8:
                practice2_results['car'] = stats_filtered_list[-3]
                practice2_results['fastest_time'] = stats_filtered_list[-2] 
                practice2_results['gap_from_1stPosition'] = 0
                practice2_results['total_laps_completed'] = stats_filtered_list[-1]
            elif len(stats_filtered_list) == 9: 
                practice2_results['car'] = stats_filtered_list[-4]
                practice2_results['fastest_time'] = stats_filtered_list[-3] 
                practice2_results['gap_from_1stPosition'] = stats_filtered_list[-2]
                practice2_results['total_laps_completed'] = stats_filtered_list[-1]
            yield practice2_results
            
        # sleep(random.uniform(0, 1))
            
    def parse_current_season_practice1_results (self, response): 
        practice1_structure =  response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[2]/div/div[3]/div[2]/table/tbody')
        practice1_elements = practice1_structure.css("tr")
        
        practice1_results = Practice1()
        practice1_results['year'] = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[2]/div/div[2]/p[1]/text()').get()[-4:]
        practice1_results['race_fullname'] = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[2]/div/div[1]/h1/text()').get()
        practice1_results['race_date'] = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[2]/div/div[2]/p[1]/text()').get()
        practice1_results['race_circuit'] = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[2]/div/div[2]/p[2]/text()').get()
        
        for indiv_driver_row in practice1_elements: 
            stats_unfiltered_list = indiv_driver_row.css("td ::text").getall()
            stats_filtered_list = [elem for elem in stats_unfiltered_list if elem != '\xa0']
            practice1_results['position'] = stats_filtered_list[0]
            practice1_results['car_number'] = stats_filtered_list[1]
            practice1_results['driver'] = stats_filtered_list[2] + " " + stats_filtered_list[3]
            if len(stats_filtered_list) == 8:
                practice1_results['car'] = stats_filtered_list[-3]
                practice1_results['fastest_time'] = stats_filtered_list[-2] 
                practice1_results['gap_from_1stPosition'] = 0
                practice1_results['total_laps_completed'] = stats_filtered_list[-1]
            elif len(stats_filtered_list) == 9: 
                practice1_results['car'] = stats_filtered_list[-4]
                practice1_results['fastest_time'] = stats_filtered_list[-3] 
                practice1_results['gap_from_1stPosition'] = stats_filtered_list[-2]
                practice1_results['total_laps_completed'] = stats_filtered_list[-1]
                
            yield practice1_results
    
    def parse_past_seasons_practice1_results (self, response): 
        practice1_structure =  response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[2]/div/div[3]/div[2]/table/tbody')
        practice1_elements = practice1_structure.css("tr")
        
        practice1_results = Practice1()
        practice1_results['year'] = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[2]/div/div[2]/p[1]/text()').get()[-4:]
        practice1_results['race_fullname'] = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[2]/div/div[1]/h1/text()').get()
        practice1_results['race_date'] = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[2]/div/div[2]/p[1]/text()').get()
        practice1_results['race_circuit'] = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[2]/div/div[2]/p[2]/text()').get()
        
        for indiv_driver_row in practice1_elements: 
            stats_unfiltered_list = indiv_driver_row.css("td ::text").getall()
            stats_filtered_list = [elem for elem in stats_unfiltered_list if elem != '\xa0']
            practice1_results['position'] = stats_filtered_list[0]
            practice1_results['car_number'] = stats_filtered_list[1]
            practice1_results['driver'] = stats_filtered_list[2] + " " + stats_filtered_list[3]
            if len(stats_filtered_list) == 8:
                practice1_results['car'] = stats_filtered_list[-3]
                practice1_results['fastest_time'] = stats_filtered_list[-2] 
                practice1_results['gap_from_1stPosition'] = 0
                practice1_results['total_laps_completed'] = stats_filtered_list[-1]
            elif len(stats_filtered_list) == 9: 
                practice1_results['car'] = stats_filtered_list[-4]
                practice1_results['fastest_time'] = stats_filtered_list[-3] 
                practice1_results['gap_from_1stPosition'] = stats_filtered_list[-2]
                practice1_results['total_laps_completed'] = stats_filtered_list[-1]
            yield practice1_results
            
        # sleep(random.uniform(0, 1))
        
    def parse_current_season_driver_standings (self, response): 
        base_url = 'https://www.formula1.com'
        driver_standings_structure = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[2]/div/div[2]/table/tbody')
        driver_standings_elements = driver_standings_structure.css("tr")
        
        driver_standings = DriverStandings()
        driver_standings['year'] = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[2]/div/div[1]/h1/text()').get()
        for indiv_driver_row in driver_standings_elements: 
            stats_unfiltered_list = indiv_driver_row.css("td ::text").getall()
            stats_filtered_list = [elem for elem in stats_unfiltered_list if elem != '\xa0']
            driver_standings['position'] = stats_filtered_list[0]
            driver_standings['driver'] = stats_filtered_list[1] + " " + stats_filtered_list[2]
            driver_standings['nationality'] = stats_filtered_list[-3]
            driver_standings['car'] = stats_filtered_list[-2]
            driver_standings['total_points'] = stats_filtered_list[-1]
            yield driver_standings
        
        drivers_structure = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[1]/details[3]/div/ul')
        drivers_elements = drivers_structure.css("li")
        for driver in drivers_elements[1:]: 
            driver_sideurl = driver.css("a ::attr(href)").get()
            official_driver_compiled_standings_url = f"{base_url}{driver_sideurl}"
            yield response.follow(official_driver_compiled_standings_url, callback=self.parse_driver_current_season_standings_progression, headers={"User-Agent" : random.choice(self.user_agent_list)}, dont_filter=True)
        
    def parse_past_seasons_driver_standings (self, response): 
        base_url = 'https://www.formula1.com'
        driver_standings_structure = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[2]/div/div[2]/table/tbody')
        driver_standings_elements = driver_standings_structure.css("tr")
        
        driver_standings = DriverStandings()
        driver_standings['year'] = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[2]/div/div[1]/h1/text()').get()
        for indiv_driver_row in driver_standings_elements: 
            stats_unfiltered_list = indiv_driver_row.css("td ::text").getall()
            stats_filtered_list = [elem for elem in stats_unfiltered_list if elem != '\xa0']
            driver_standings['position'] = stats_filtered_list[0]
            driver_standings['driver'] = stats_filtered_list[1] + " " + stats_filtered_list[2]
            driver_standings['nationality'] = stats_filtered_list[-3]
            driver_standings['car'] = stats_filtered_list[-2]
            driver_standings['total_points'] = stats_filtered_list[-1]
            yield driver_standings
        
        # sleep(random.uniform(0, 1))
        
        drivers_structure = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[1]/details[3]/div/ul')
        drivers_elements = drivers_structure.css("li")
        for driver in drivers_elements[1:]: 
            driver_sideurl = driver.css("a ::attr(href)").get()
            official_driver_compiled_standings_url = f"{base_url}{driver_sideurl}"
            yield response.follow(official_driver_compiled_standings_url, callback=self.parse_driver_past_seasons_standings_progression, headers={"User-Agent" : random.choice(self.user_agent_list)}, dont_filter=True)
    
    def parse_current_season_team_standings (self, response): 
        base_url = 'https://www.formula1.com'
        constructor_standings_structure = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[2]/div/div[2]/table/tbody')
        constructor_standings_elements = constructor_standings_structure.css("tr")
        
        constructor_standings = ConstructorStandings()
        constructor_standings['year'] = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[2]/div/div[1]/h1/text()').get()
        for indiv_team_row in constructor_standings_elements: 
            stats_list = indiv_team_row.css("td ::text").getall()
            constructor_standings['position'] = stats_list[0]
            constructor_standings['team'] = stats_list[1]
            constructor_standings['total_points'] = stats_list[-1]
            yield constructor_standings
        
        teams_structure = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[1]/details[3]/div/ul')
        teams_elements = teams_structure.css("li")
        for team in teams_elements[1:]: 
            team_sideurl = team.css("a ::attr(href)").get()
            official_team_race_standings_url = f"{base_url}{team_sideurl}"
            yield response.follow(official_team_race_standings_url, callback=self.get_team_current_season_standings_progression, headers={"User-Agent" : random.choice(self.user_agent_list)}, dont_filter=True)
            
                
    def parse_past_seasons_team_standings (self, response):
        base_url = 'https://www.formula1.com'
        constructor_standings_structure = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[2]/div/div[2]/table/tbody')
        constructor_standings_elements = constructor_standings_structure.css("tr")
        
        constructor_standings = ConstructorStandings()
        constructor_standings['year'] = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[2]/div/div[1]/h1/text()').get()
        for indiv_team_row in constructor_standings_elements: 
            stats_list = indiv_team_row.css("td ::text").getall()
            constructor_standings['position'] = stats_list[0]
            constructor_standings['team'] = stats_list[1]
            constructor_standings['total_points'] = stats_list[-1]
            yield constructor_standings
        
        # sleep(random.uniform(0, 1))
    
        teams_structure = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[1]/details[3]/div/ul')
        teams_elements = teams_structure.css("li")
        for team in teams_elements[1:]: 
            team_sideurl = team.css("a ::attr(href)").get()
            official_team_race_standings_url = f"{base_url}{team_sideurl}"
            yield response.follow(official_team_race_standings_url, callback=self.get_team_past_seasons_standings_progression, headers={"User-Agent" : random.choice(self.user_agent_list)}, dont_filter=True)
            
    def parse_driver_current_season_standings_progression (self, response): 
        driver_race_progression_structure = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[2]/div/div[2]/table/tbody')
        driver_race_progression_elements = driver_race_progression_structure.css("tr")
        
        driver_race_standings_progression = DriverRaceStandingsProgression()
        driver_race_standings_progression['year'] = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[2]/div/div[1]/h1/text()').get()[:4]
        title_list = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[2]/div/div[1]/h1/text()').get().split(' ')
        retrieved_name_list_DT = [elem for elem in title_list if elem!= 'Standings:' and elem != 'Driver' and elem.isdigit() == False]
        driver_race_standings_progression['name'] = ' '.join(retrieved_name_list_DT)
        for indiv_race in driver_race_progression_elements: 
            stats_list = indiv_race.css("td ::text").getall()
            driver_race_standings_progression['grand_prix'] = stats_list[0]
            driver_race_standings_progression['race_date'] = stats_list[1]
            driver_race_standings_progression['car'] = stats_list[2]
            
            if len(stats_list) == 4: 
                driver_race_standings_progression['race_position'] = stats_list[-1]
                driver_race_standings_progression['points'] = '0'
            elif len(stats_list) == 5:
                driver_race_standings_progression['race_position'] = stats_list[-2]
                driver_race_standings_progression['points'] = stats_list[-1]
            
            yield driver_race_standings_progression
        
    def parse_driver_past_seasons_standings_progression (self, response):
        driver_race_progression_structure = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[2]/div/div[2]/table/tbody')
        driver_race_progression_elements = driver_race_progression_structure.css("tr")
        
        driver_race_standings_progression = DriverRaceStandingsProgression()
        driver_race_standings_progression['year'] = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[2]/div/div[1]/h1/text()').get()[:4]
        title_list = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[2]/div/div[1]/h1/text()').get().split()
        retrieved_name_list_DT = [elem for elem in title_list if elem!= 'Standings:' and elem != 'Driver' and elem.isdigit() == False]
        driver_race_standings_progression['name'] = ' '.join(retrieved_name_list_DT)
        for indiv_race in driver_race_progression_elements: 
            stats_list = indiv_race.css("td ::text").getall()
            driver_race_standings_progression['grand_prix'] = stats_list[0]
            driver_race_standings_progression['race_date'] = stats_list[1]
            driver_race_standings_progression['car'] = stats_list[2]
            
            if len(stats_list) == 4: 
                driver_race_standings_progression['race_position'] = stats_list[-1]
                driver_race_standings_progression['points'] = '0'
            elif len(stats_list) == 5:
                driver_race_standings_progression['race_position'] = stats_list[-2]
                driver_race_standings_progression['points'] = stats_list[-1]
            
            yield driver_race_standings_progression
        
        # sleep(random.uniform(0, 1))
        
    def get_team_current_season_standings_progression (self, response): 
        team_structure = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[2]/div/div[2]/table/tbody')
        team_elements = team_structure.css("tr")
        
        team_race_standings_progression = TeamRaceStandingsProgression()
        title_list = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[2]/div/div[1]/h1/text()').get().split()
        retrieved_team_name_list_DT = [elem for elem in title_list if elem!= 'Standings:' and elem != 'Constructor' and elem.isdigit() == False]
        team_race_standings_progression['year'] = title_list[0]
        team_race_standings_progression['team_name'] = " ".join(retrieved_team_name_list_DT)
        
        for indiv_race in team_elements: 
            stats_list = indiv_race.css("td ::text").getall()
            team_race_standings_progression['grand_prix'] = stats_list[0]
            team_race_standings_progression['race_date'] = stats_list[1]
            team_race_standings_progression['points'] = stats_list[-1]
            yield team_race_standings_progression

    def get_team_past_seasons_standings_progression (self, response): 
        team_structure = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[2]/div/div[2]/table/tbody')
        team_elements = team_structure.css("tr")
        
        team_race_standings_progression = TeamRaceStandingsProgression()
        title_list = response.xpath('//*[@id="maincontent"]/div/div[2]/main/div[2]/div[2]/div/div[1]/h1/text()').get().split()
        retrieved_team_name_list_DT = [elem for elem in title_list if elem!= 'Standings:' and elem != 'Constructor' and elem.isdigit() == False]
        team_race_standings_progression['year'] = title_list[0]
        team_race_standings_progression['team_name'] = " ".join(retrieved_team_name_list_DT)
        
        for indiv_race in team_elements: 
            stats_list = indiv_race.css("td ::text").getall()
            team_race_standings_progression['grand_prix'] = stats_list[0]
            team_race_standings_progression['race_date'] = stats_list[1]
            team_race_standings_progression['points'] = stats_list[-1]
            yield team_race_standings_progression

        # sleep(random.uniform(0, 1))
    
    def parse_drivers (self, response): 
        base_url = 'https://www.formula1.com'
        driver_cards_structure = response.xpath('//*[@id="maincontent"]/main/div/div/div[4]')
        driver_cards_sideurls = driver_cards_structure.css("a ::attr(href)").getall()
        for indiv_driver_sideurl in driver_cards_sideurls: 
            driver_sideurl = f"{base_url}{indiv_driver_sideurl}"
            yield response.follow(driver_sideurl, callback=self.get_current_season_individual_driver_information, headers={"User-Agent" : random.choice(self.user_agent_list)}, dont_filter=True)
    
    def get_current_season_individual_driver_information (self, response): 
        driver_information_table = response.xpath('//*[@id="maincontent"]/main/div/div/div[1]/div/div[2]/dl')
        driver_information_list = driver_information_table.css("dd ::text").getall()
        
        driver_information = DriverInformation()
        driver_information['name'] = response.xpath('//*[@id="maincontent"]/main/div/div/div[1]/figure/figcaption/div/h1/text()').get()
        driver_information['team_name'] = driver_information_list[0]
        driver_information['country'] = driver_information_list[1]
        driver_information['podiums'] = driver_information_list[2]
        driver_information['lifetime_points'] = driver_information_list[3]
        driver_information['grand_prix_participated'] = driver_information_list[4]
        driver_information['world_driver_championships'] = driver_information_list[5]
        driver_information['highest_race_finish'] = driver_information_list[-4]
        driver_information['highest_grid_position'] = driver_information_list[-3]
        driver_information['date_of_birth'] = driver_information_list[-2]
        driver_information['place_of_birth'] = driver_information_list[-1]
        yield driver_information
    