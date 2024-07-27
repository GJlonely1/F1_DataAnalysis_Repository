# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from F1_WebScrape.items import Stories, RacingSchedule, OverallSingleSeasonRaceResults, IndividualRaceResults, IndividualRaceFastestLaps, DriverPitStopSummary, StartingGrid, Qualifying, Practice3, Practice2, Practice1, DriverStandings, ConstructorStandings
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
                item.get('position', ''),
                item.get('car_number', ''),
                item.get('driver', ''),
                item.get('car', ''),
                item.get('laps', ''),
                item.get('time_or_retired', ''),
                item.get('points', ''),
            ])
        return item

class IndividualRaceFastestLapsPipeline: 
    def open_spider(self, spider):
        self.json_file = open('individual_race_fastest_laps.json', 'w')
        self.csv_file = open('individual_race_fastest_laps.csv', 'w', newline='')
        self.csv_writer = csv.writer(self.csv_file)
        self.json_file.write('[')
        self.first_item = True
    
    def close_spider(self, spider):
        self.json_file.write(']')
        self.json_file.close()
        self.csv_file.close()
    
    def process_item(self, item, spider):
        if isinstance(item, IndividualRaceFastestLaps):
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
                item.get('position', ''),
                item.get('car_number', ''),
                item.get('driver', ''),
                item.get('car', ''),
                item.get('fastest_lap_number', ''),
                item.get('time_of_day', ''),
                item.get('fastest_time', ''),
                item.get('average_speed', ''),
            ])
        return item

class IndividualRacePitStopSummaryPipeline: 
    def open_spider(self, spider):
        self.json_file = open('individual_race_pitstop_summary.json', 'w')
        self.csv_file = open('individual_race_pitstop_summary.csv', 'w', newline='')
        self.csv_writer = csv.writer(self.csv_file)
        self.json_file.write('[')
        self.first_item = True
    
    def close_spider(self, spider):
        self.json_file.write(']')
        self.json_file.close()
        self.csv_file.close()
    
    def process_item(self, item, spider):
        if isinstance(item, DriverPitStopSummary):
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
                item.get('pitstop_count', ''),
                item.get('car_number', ''),
                item.get('driver', ''),
                item.get('car', ''),
                item.get('pit_stop_lap_number', ''),
                item.get('time_of_day_for_pitstop', ''),
                item.get('pit_stop_duration', ''),
                item.get('total_pitstop_duration', ''),
            ])
        return item
    
class StartingGridPipeline:
    def open_spider(self, spider):
        self.json_file = open('indiv_race_starting_grid.json', 'w')
        self.csv_file = open('indiv_race_starting_grid.csv', 'w', newline='')
        self.csv_writer = csv.writer(self.csv_file)
        self.json_file.write('[')
        self.first_item = True
    
    def close_spider(self, spider):
        self.json_file.write(']')
        self.json_file.close()
        self.csv_file.close()
    
    def process_item(self, item, spider):
        if isinstance(item, StartingGrid):
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
                item.get('position', ''),
                item.get('car_number', ''),
                item.get('driver', ''),
                item.get('car', ''),
                item.get('qualifying_time', ''),
            ])
        return item
    
class QualificationResultsPipeline: 
    def open_spider(self, spider):
        self.json_file = open('race_qualification_results.json', 'w')
        self.csv_file = open('race_qualification_results.csv', 'w', newline='')
        self.csv_writer = csv.writer(self.csv_file)
        self.json_file.write('[')
        self.first_item = True
    
    def close_spider(self, spider):
        self.json_file.write(']')
        self.json_file.close()
        self.csv_file.close()
    
    def process_item(self, item, spider):
        if isinstance(item, Qualifying):
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
                item.get('position', ''),
                item.get('car_number', ''),
                item.get('driver', ''),
                item.get('car', ''),
                item.get('Q1_time', ''),
                item.get('Q2_time', ''),
                item.get('Q3_time', ''),
                item.get('Final_Qualifying_time', ''),
                item.get('total_laps_completed', ''),
            ])
        return item

class Practice3Pipeline: 
    def open_spider(self, spider):
        self.json_file = open('practice3_results.json', 'w')
        self.csv_file = open('practice3_results.csv', 'w', newline='')
        self.csv_writer = csv.writer(self.csv_file)
        self.json_file.write('[')
        self.first_item = True
    
    def close_spider(self, spider):
        self.json_file.write(']')
        self.json_file.close()
        self.csv_file.close()
    
    def process_item(self, item, spider):
        if isinstance(item, Practice3):
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
                item.get('position', ''),
                item.get('car_number', ''),
                item.get('driver', ''),
                item.get('car', ''),
                item.get('fastest_time', ''),
                item.get('gap_from_1stPosition', ''),
                item.get('total_laps_completed', ''),
            ])
        return item

class Practice2Pipeline: 
    def open_spider(self, spider):
        self.json_file = open('practice2_results.json', 'w')
        self.csv_file = open('practice2_results.csv', 'w', newline='')
        self.csv_writer = csv.writer(self.csv_file)
        self.json_file.write('[')
        self.first_item = True
    
    def close_spider(self, spider):
        self.json_file.write(']')
        self.json_file.close()
        self.csv_file.close()
    
    def process_item(self, item, spider):
        if isinstance(item, Practice2):
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
                item.get('position', ''),
                item.get('car_number', ''),
                item.get('driver', ''),
                item.get('car', ''),
                item.get('fastest_time', ''),
                item.get('gap_from_1stPosition', ''),
                item.get('total_laps_completed', ''),
            ])
        return item

class Practice1Pipeline:
    def open_spider(self, spider):
        self.json_file = open('practice1_results.json', 'w')
        self.csv_file = open('practice1_results.csv', 'w', newline='')
        self.csv_writer = csv.writer(self.csv_file)
        self.json_file.write('[')
        self.first_item = True
    
    def close_spider(self, spider):
        self.json_file.write(']')
        self.json_file.close()
        self.csv_file.close()
    
    def process_item(self, item, spider):
        if isinstance(item, Practice1):
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
                item.get('position', ''),
                item.get('car_number', ''),
                item.get('driver', ''),
                item.get('car', ''),
                item.get('fastest_time', ''),
                item.get('gap_from_1stPosition', ''),
                item.get('total_laps_completed', ''),
            ])
        return item
    
class DriverStandingsPipeline: 
    def open_spider(self, spider):
        self.json_file = open('Driver_Standings.json', 'w')
        self.csv_file = open('Driver_Standings.csv', 'w', newline='')
        self.csv_writer = csv.writer(self.csv_file)
        self.json_file.write('[')
        self.first_item = True
    
    def close_spider(self, spider):
        self.json_file.write(']')
        self.json_file.close()
        self.csv_file.close()
    
    def process_item(self, item, spider):
        if isinstance(item, DriverStandings):
            if not self.first_item: 
                self.json_file.write(',')
            # Write to JSON
            json.dump(dict(item), self.json_file, ensure_ascii=False)
            self.first_item = False
        
            # Write to CSV
            self.csv_writer.writerow([
                item.get('year', ''),
                item.get('position', ''),
                item.get('driver', ''),
                item.get('car', ''),
                item.get('nationality', ''),
                item.get('total_points', ''),
            ])
        return item

class ConstructorStandingsPipeline:
    def open_spider(self, spider):
        self.json_file = open('Constructor_Standings.json', 'w')
        self.csv_file = open('Constructor_Standings.csv', 'w', newline='')
        self.csv_writer = csv.writer(self.csv_file)
        self.json_file.write('[')
        self.first_item = True
    
    def close_spider(self, spider):
        self.json_file.write(']')
        self.json_file.close()
        self.csv_file.close()
    
    def process_item(self, item, spider):
        if isinstance(item, ConstructorStandings):
            if not self.first_item: 
                self.json_file.write(',')
            # Write to JSON
            json.dump(dict(item), self.json_file, ensure_ascii=False)
            self.first_item = False
        
            # Write to CSV
            self.csv_writer.writerow([
                item.get('year', ''),
                item.get('position', ''),
                item.get('team', ''),
                item.get('total_points', ''),
            ])
        return item