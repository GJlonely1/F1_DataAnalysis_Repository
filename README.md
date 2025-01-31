
# Formula 1 Data Analysis Project

## Project Description
This project focuses on comprehensive data analysis of Formula 1 racing, covering seasons from 1950 to 2024. It involves web scraping, data processing, exploratory data analysis (EDA), and visualization through an interactive dashboard.

## Data Collection
Data was extracted from the official Formula 1 website using:
- Python Scrapy Framework
- Selenium for automation

## Dataset
The collected dataset includes:
- F1 Season data (1950 - 2024)
- Constructor Standings Information
- Driver Personal Details
- Driver Pit Stop Summary
- Driver Race Standings
- Grand Prix Locations
- Driver Individual Race Fastest Laps
- Driver Individual Race Results
- Driver Overall Single Season Results
- Practice 1, 2, and 3 Results
- Qualifying Results
- Driver Starting Grid
- Race Circuit Information
- Formula 1 Racing Schedule
- Formula 1 Latest Stories
- Constructor Race Standings

## Data Storage
Data is stored in:
- CSV files
- JSON files

## Data Processing
The project involves:
- Data wrangling
- Data cleaning
- Exploratory Data Analysis (EDA)
- Feature engineering

## Visualization
A 3-page interactive and dynamic dashboard was created using Power BI.

## Objective
The main objectives of this project are:
1. Facilitate data extraction through web scraping
2. Consolidate raw data into meaningful and insightful information
3. Present data through dynamic visualizations and dashboards for all stakeholders

## Getting Started
### Prerequisites
- Python 3.7 or higher
- Power BI Desktop (for viewing dashboards)

### Installation
1. Clone the repository: 
git clone https://github.com/GJlonely1/f1_dataanalysis_repository.git
cd F1_WebScrape
cd F1_WebScrape

2. Create a virtual environment (optional but recommended):
python -m venv venv
source venv/bin/activate  # On Windows, use venv\Scripts\activate

3. Install required Python libraries:

### Running the Web Scraper
To collect the most up-to-date data:

1. Navigate to the scraping directory:
cd spiders
scrapy crawl F1

This will update the CSV and JSON files in the `data` directory.

### Viewing the Dashboard
1. Open Power BI Desktop
2. Open the file `F1_Analysis_Dashboard.pbix` from this repository
3. If prompted, update the data source paths to match your local directory structure

Note: The Power BI file includes pre-processed data up to [specify date]. For the most recent data, you may need to run the data processing scripts after scraping new data.

## Dependencies
(List of libraries and tools required for the project, including Scrapy, Selenium, and Power BI)

## Acknowledgments
- Official Formula 1 website for providing the source data
- (Any other acknowledgments or credits)