# Scrapy settings for F1_WebScrape project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "F1_WebScrape"

SPIDER_MODULES = ["F1_WebScrape.spiders"]
NEWSPIDER_MODULE = "F1_WebScrape.spiders"


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "F1_WebScrape (+http://www.yourdomain.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

FEEDS = {
   'all_news.json': {
      'format': 'json',
      'overwrite': True,
      'encoding': 'utf8',
   },
   'past_present_season_results.json': {
      'format': 'json',
      'overwrite': True,
      'encoding': 'utf8',
   },
   'past_present_season_results.csv': {
      'format': 'csv',
      'overwrite': True,
      'encoding': 'utf8',
   },
   'race_schedule.json' : {
      'format': 'json',
      'overwrite': True,
      'encoding': 'utf8',
   }, 
   'race_schedule.csv' : {
      'format': 'csv',
      'overwrite': True,
      'encoding': 'utf8',
   },
   'individual_race_results.json' : {
      'format': 'json',
      'overwrite': True,
      'encoding': 'utf8',
   },
   'individual_race_results.csv' : {
      'format': 'csv',
      'overwrite': True,
      'encoding': 'utf8',
   },
   'individual_race_fastest_laps.json' : {
      'format': 'json',
      'overwrite': True,
      'encoding': 'utf8',
   }, 
   'individual_race_fastest_laps.csv' : {
      'format': 'csv',
      'overwrite': True,
      'encoding': 'utf8',
   }, 
   'individual_race_pitstop_summary.json' : {
      'format': 'json',
      'overwrite': True,
      'encoding': 'utf8',
   }, 
   'individual_race_pitstop_summary.csv' : {
      'format': 'csv',
      'overwrite': True,
      'encoding': 'utf8',
   }, 
   'indiv_race_starting_grid.json' : {
      'format': 'json',
      'overwrite': True,
      'encoding': 'utf8',
   },
   'indiv_race_starting_grid.csv' : {
      'format': 'csv',
      'overwrite': True,
      'encoding': 'utf8',
   },
   'race_qualification_results.json' : {
      'format': 'json',
      'overwrite': True,
      'encoding': 'utf8',
   }, 
   'race_qualification_results.csv' : {
      'format': 'csv',
      'overwrite': True,
      'encoding': 'utf8',
   }, 
}
ITEM_PIPELINES = {
   'F1_WebScrape.pipelines.CustomFilePipeline': 300,
   'F1_WebScrape.pipelines.AllNewsPipeline': 1,
   'F1_WebScrape.pipelines.PastPresentSeasonResultsPipeline': 2,
   'F1_WebScrape.pipelines.RaceSchedulePipeline' : 3, 
   'F1_WebScrape.pipelines.IndividualRaceResultsPipeline' : 4,
   'F1_WebScrape.pipelines.IndividualRaceFastestLapsPipeline' : 5,
   'F1_WebScrape.pipelines.IndividualRacePitStopSummaryPipeline' : 6,
   'F1_WebScrape.pipelines.StartingGridPipeline' : 7,
   'F1_WebScrape.pipelines.QualificationResultsPipeline' : 8,
}


from shutil import which

SELENIUM_DRIVER_NAME = 'chrome'
# SELENIUM_DRIVER_EXECUTABLE_PATH = None
SELENIUM_DRIVER_ARGUMENTS = ['--headless']  # '--headless' if using headless mode


# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settngs.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
   "F1_WebScrape.middlewares.F1WebscrapeSpiderMiddleware": 543,
}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   "F1_WebScrape.middlewares.F1WebscrapeDownloaderMiddleware": 543,
   'scrapy_selenium.SeleniumMiddleware': 800

}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    "F1_WebScrape.pipelines.F1WebscrapePipeline": 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
