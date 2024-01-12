# Website scraper for Lincoln WI website
## Usage
This project uses Python 3.12 and the scrapy web-crawling framework

Basic command to run spider:

- First cd into `lincolnwiscraper` 

- Then use `scrapy crawl lincolnwispider -O output.csv` to generate a csv file called output.csv (filename can be changed)

- Number of pages to be crawled can be specified with an additional argument called total_pages

- For example `scrapy crawl lincolnwispider -a total_pages=2 -O output.csv` will scrape 2 pages of the website

## Output

This spider was designed to generate a .csv output file. 
A sample output file called output.csv is provided in the main folder.

## Potential future updates

- Discuss document type categorization (for example, how should hyperlinks without text, amended documents, cancelled agendas, revised minutes be categorized)
- Improve unit testing class to test for different configurations of websites (for example, missing field types) to ensure the script works even if the website format is changed
- Add online testing
- Sort CSV file by date after creating it
