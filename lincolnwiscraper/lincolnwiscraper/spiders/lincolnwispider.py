import scrapy
import datetime
import csv

class LincolnwispiderSpider(scrapy.Spider):
    name = "lincolnwispider"
    allowed_domains = ["co.lincoln.wi.us"]
    start_urls = ["https://co.lincoln.wi.us/meetings"]

    def parse(self, response):
        date = response.css("td.views-field-field-calendar-date span.date-display-single::text").get()
        title = response.css("td.views-field-title::text").get()
        self.save_to_csv([["date", "meeting_title", "category", "URL"], [date, title, "", ""]])

    def generate_timestamp(self) -> str:
        return datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    def save_to_csv(self, contents):
        file_name = "CO_LINCOLN_WI_US_MEETINGS-metadata-" + self.generate_timestamp() + ".csv"
        with open(file_name, 'w', newline='') as file:
            writer = csv.writer(file)
            for i in range(len(contents)):
                writer.writerow(contents[i])

