import scrapy
import datetime
import csv

class LincolnwispiderSpider(scrapy.Spider):
    name = "lincolnwispider"
    allowed_domains = ["co.lincoln.wi.us"]
    start_urls = ["https://co.lincoln.wi.us/meetings"]

    def parse(self, response):
        rows = response.css("tbody tr")
        content = [["date", "meeting_title", "category", "URL"]]

        for row in rows:
            date = row.css("td.views-field-field-calendar-date span.date-display-single::text").get()
            title = row.css("td.views-field-title::text").get().replace("\r\n            ","").replace("          ","")
            content += self.parse_documents(date, title, row)

        self.save_to_csv(content)

    # Loop through each individual agenda element
    def parse_documents(self, date, title, row) -> []:
        document_data = []
        agendas = row.css("td.views-field-field-agendas div ul li")
        for agenda in agendas:
            category = agenda.css("a::text").get()  # Link text
            category = "agenda" if category is None or  "agenda" in category.lower() else "other"
            url = agenda.css("a").attrib["href"]
            document_data.append([date, title, category, url])

        packets = row.css("td.views-field-field-packets a")
        for packet in packets:
            category = packet.css("a::text").get()  # Link text
            category = "agenda_packet" if category is None or "packet" == category.lower() or "amended" in category.lower() else "other"
            url = packet.css("a").attrib["href"]
            document_data.append([date, title, category, url])

        minutes = row.css("td.views-field-field-minutes div ul li")
        for minute in minutes:
            category = minute.css("a::text").get()  # Link text
            category = "minutes" if category is None or "minutes" == category.lower() else "other"
            url = minute.css("a").attrib["href"]
            document_data.append([date, title, category, url])

        return document_data

    # Generate a timestamp for the filename
    def generate_timestamp(self) -> str:
        return datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Save data to csv file
    def save_to_csv(self, contents):
        file_name = "CO_LINCOLN_WI_US_MEETINGS-metadata-" + self.generate_timestamp() + ".csv"
        with open(file_name, 'w', newline='') as file:
            writer = csv.writer(file)
            for i in range(len(contents)):
                writer.writerow(contents[i])

