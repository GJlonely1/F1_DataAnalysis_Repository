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

class OverallSingleSeasonRaceResults(scrapy.Item):
    year = scrapy.Field() 
    grand_prix = scrapy.Field()
    date = scrapy.Field()
    race_winner = scrapy.Field()
    car = scrapy.Field()
    laps = scrapy.Field()
    time = scrapy.Field()

class IndividualRaceResults(scrapy.Item):
    year = scrapy.Field()
    race_fullname = scrapy.Field()
    race_date = scrapy.Field()
    race_circuit = scrapy.Field()
    position = scrapy.Field()
    car_number = scrapy.Field() 
    driver = scrapy.Field()
    car = scrapy.Field()
    laps = scrapy.Field() 
    time_or_retired = scrapy.Field() 
    points = scrapy.Field() 

class IndividualRaceFastestLaps(scrapy.Item): 
    year = scrapy.Field()
    race_fullname = scrapy.Field()
    race_date = scrapy.Field()
    race_circuit = scrapy.Field() 
    position = scrapy.Field()
    car_number = scrapy.Field() 
    driver = scrapy.Field()
    car = scrapy.Field()
    fastest_lap_number = scrapy.Field() 
    time_of_day = scrapy.Field() 
    fastest_time = scrapy.Field()
    average_speed = scrapy.Field( )

class DriverPitStopSummary(scrapy.Item): 
    year = scrapy.Field()
    race_fullname = scrapy.Field()
    race_date = scrapy.Field()
    race_circuit = scrapy.Field()
    pitstop_count = scrapy.Field() 
    car_number = scrapy.Field()
    driver = scrapy.Field()
    car = scrapy.Field()
    pit_stop_lap_number = scrapy.Field()
    time_of_day_for_pitstop = scrapy.Field()
    pit_stop_duration = scrapy.Field()
    # total_pitstop_duration = pitstop_count * pitstop_duration
    total_pitstop_duration = scrapy.Field()
    
class StartingGrid(scrapy.Item): 
    year = scrapy.Field()
    race_fullname = scrapy.Field()
    race_date = scrapy.Field()
    race_circuit = scrapy.Field()
    position = scrapy.Field()
    car_number = scrapy.Field()
    driver = scrapy.Field()
    car = scrapy.Field()
    qualifying_time = scrapy.Field()

class Qualifying(scrapy.Item):
    year = scrapy.Field()
    race_fullname = scrapy.Field()
    race_date = scrapy.Field()
    race_circuit = scrapy.Field()
    position = scrapy.Field()
    car_number = scrapy.Field()
    driver = scrapy.Field()
    car = scrapy.Field()
    Final_Qualifying_time = scrapy.Field()
    Q1_time = scrapy.Field()
    Q2_time = scrapy.Field()
    Q3_time = scrapy.Field()
    total_laps_completed = scrapy.Field()

class Practice3 (scrapy.Item): 
    year = scrapy.Field()
    race_fullname = scrapy.Field()
    race_date = scrapy.Field()
    race_circuit = scrapy.Field()
    position = scrapy.Field()
    car_number = scrapy.Field()
    driver = scrapy.Field()
    car = scrapy.Field()
    fastest_time = scrapy.Field()
    gap_from_1stPosition = scrapy.Field()
    total_laps_completed = scrapy.Field()

class Practice2 (scrapy.Item):
    year = scrapy.Field()
    race_fullname = scrapy.Field()
    race_date = scrapy.Field()
    race_circuit = scrapy.Field()
    position = scrapy.Field()
    car_number = scrapy.Field()
    driver = scrapy.Field()
    car = scrapy.Field()
    fastest_time = scrapy.Field()
    gap_from_1stPosition = scrapy.Field()
    total_laps_completed = scrapy.Field()

class Practice1 (scrapy.Item):
    year = scrapy.Field()
    race_fullname = scrapy.Field()
    race_date = scrapy.Field()
    race_circuit = scrapy.Field()
    position = scrapy.Field()
    car_number = scrapy.Field()
    driver = scrapy.Field()
    car = scrapy.Field()
    fastest_time = scrapy.Field()
    gap_from_1stPosition = scrapy.Field()
    total_laps_completed = scrapy.Field()

class DriverStandings(scrapy.Item): 
    year = scrapy.Field()
    position = scrapy.Field()
    driver = scrapy.Field()
    nationality = scrapy.Field()
    car = scrapy.Field()
    total_points = scrapy.Field()

class ConstructorStandings (scrapy.Item): 
    year = scrapy.Field()
    position = scrapy.Field()
    team = scrapy.Field()
    total_points = scrapy.Field()
    