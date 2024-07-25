# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from F1_WebScrape.items import Stories, RacingSchedule, OverallSingleSeasonRaceResults
import json 
import csv

class F1WebscrapePipeline:
    def process_item(self, item, spider):
        return item


class AllNewsPipeline:
    def open_spider(self, spider):
        self.json_file = open('all_news.json', 'w')
        self.json_file.write('[')
        self.first_item = True

    def close_spider(self, spider):
        self.json_file.write(']')
        self.json_file.close()

    def process_item(self, item, spider):
        if isinstance(item, Stories):
            if not self.first_item: 
                self.json_file.write(',')
            # Write to JSON
            json.dump(dict(item), self.json_file, ensure_ascii=False)
            self.first_item = False
        return item

class PastPresentSeasonResultsPipeline:
    def open_spider(self, spider):
        self.json_file = open('past_present_season_results.json', 'w')
        self.csv_file = open('past_present_season_results.csv', 'w', newline='')
        self.csv_writer = csv.writer(self.csv_file)
        self.json_file.write('[')
        self.first_item = True

    def close_spider(self, spider):
        self.json_file.write(']')
        self.json_file.close()
        self.csv_file.close()

    def process_item(self, item, spider):
        if isinstance(item, OverallSingleSeasonRaceResults):
            if not self.first_item: 
                self.json_file.write(',')
            # Write to JSON
            json.dump(dict(item), self.json_file, ensure_ascii=False)
            self.first_item = False
        
            # Write to CSV
            self.csv_writer.writerow([
                item.get('year', ''),
                item.get('grand_prix', ''),
                item.get('date', ''),
                item.get('race_winner', ''),
                item.get('car', ''),
                item.get('laps', ''),
                item.get('time', ''),
            ])
        return item
    
class RaceSchedulePipeline:
    def open_spider(self, spider):
        self.json_file = open('race_schedule.json', 'w')
        self.csv_file = open('race_schedule.csv', 'w', newline='')
        self.csv_writer = csv.writer(self.csv_file)
        self.json_file.write('[')
        self.first_item = True
    
    def close_spider(self, spider):
        self.json_file.write(']')
        self.json_file.close()
        self.csv_file.close()

    def process_item(self, item, spider):
        if isinstance(item, RacingSchedule):
            if not self.first_item: 
                self.json_file.write(',')
            # Write to JSON
            json.dump(dict(item), self.json_file, ensure_ascii=False)
            self.first_item = False
        
            # Write to CSV
            self.csv_writer.writerow([
                item.get('race_round', ''),
                item.get('race_url', ''),
                item.get('race_date', ''),
                item.get('location', ''),
                item.get('race_fullname', ''),
            ])
        return item