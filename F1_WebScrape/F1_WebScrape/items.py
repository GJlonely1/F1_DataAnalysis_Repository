# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class F1WebscrapeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class Stories(scrapy.Item): 
    story_name = scrapy.Field() 
    story_url = scrapy.Field() 
    story_content = scrapy.Field()

class RacingSchedule(scrapy.Item): 
    race_round = scrapy.Field()
    race_url = scrapy.Field()
    race_date = scrapy.Field()
    location = scrapy.Field()
    race_fullname = scrapy.Field()
