# Website scraper for Lincoln WI website
## Usage
This project uses Python 3.12 and the scrapy web-crawling framework

Basic command to run spider:

- First cd into `lincolnwiscraper` 

- Then use `scrapy crawl lincolnwispider -O output.csv` to generate a csv file called output.csv (filename can be changed)

- Number of pages to be crawled can be specified with an additional argument called total_pages

- For example `scrapy crawl lincolnwispider -a total_pages=2 -O output.csv`