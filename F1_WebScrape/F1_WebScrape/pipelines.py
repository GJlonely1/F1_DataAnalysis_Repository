# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from F1_WebScrape.items import Stories, RacingSchedule, OverallSingleSeasonRaceResults, IndividualRaceResults
import json 
import csv
import os

class CustomFilePipeline:
    def open_spider(self, spider):
        self.files = {}
        self.exporters = {}

    def close_spider(self, spider):
        for exporter in self.exporters.values():
            exporter.finish_exporting()
        for file in self.files.values():
            file.close()

    def _initialize_exporter(self, file_format, file_path):
        if file_format == 'json':
            file = open(file_path, 'w', encoding='utf8')
            exporter = json.JSONEncoder()
        elif file_format == 'csv':
            file = open(file_path, 'w', encoding='utf8', newline='')
            exporter = csv.writer(file)
        else:
            raise ValueError(f"Unsupported file format: {file_format}")
        
        self.files[file_path] = file
        self.exporters[file_path] = exporter

    def process_item(self, item, spider):
        item_type = type(item).__name__.lower()
        file_formats = ['json', 'csv']
        
        for file_format in file_formats:
            file_path = f'{item_type}.{file_format}'
            if file_path not in self.files:
                self._initialize_exporter(file_format, file_path)
            
            exporter = self.exporters[file_path]
            if file_format == 'json':
                json.dump(dict(item), self.files[file_path], ensure_ascii=False)
                self.files[file_path].write('\n')
            elif file_format == 'csv':
                if os.stat(file_path).st_size == 0:
                    exporter.writerow(item.keys())
                exporter.writerow(item.values())
        
        return item

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

class IndividualRaceResultsPipeline:
    def open_spider(self, spider):
        self.json_file = open('individual_race_results.json', 'w')
        self.csv_file = open('individual_race_results.csv', 'w', newline='')
        self.csv_writer = csv.writer(self.csv_file)
        self.json_file.write('[')
        self.first_item = True
    
    def close_spider(self, spider):
        self.json_file.write(']')
        self.json_file.close()
        self.csv_file.close()

    def process_item(self, item, spider):
        if isinstance(item, IndividualRaceResults):
            if not self.first_item: 
                self.json_file.write(',')
            # Write to JSON
            json.dump(dict(item), self.json_file, ensure_ascii=False)
            self.first_item = False
        
            # Write to CSV
            self.csv_writer.writerow([
                item.get('year', ''),
                item.get('race_fullname', ''),
                item.get('race_date', ''),
                item.get('race_circuit', ''),
                item.get('race_type', ''),
                item.get('position', ''),
                item.get('car_number', ''),
                item.get('driver', ''),
                item.get('car', ''),
                item.get('laps', ''),
                item.get('time_or_retired', ''),
                item.get('points', ''),
            ])
        return item