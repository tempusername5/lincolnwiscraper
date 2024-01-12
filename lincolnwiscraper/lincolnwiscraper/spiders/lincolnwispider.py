import scrapy
import datetime
import csv

class LincolnwispiderSpider(scrapy.Spider):
    name = "lincolnwispider"
    allowed_domains = ["co.lincoln.wi.us"]
    start_urls = ["https://co.lincoln.wi.us/meetings"]
    start_url = "https://co.lincoln.wi.us/meetings"

    # Allow additional argument in crawl command for number of pages
    def __init__(self, total_pages=2, **kwargs):
        self.total_pages = total_pages
        super().__init__(**kwargs)

    # Go through each page (specified in constructor)
    def start_requests(self):
        for i in range(int(self.total_pages)):
            yield scrapy.Request(self.start_url + "?page=" + str(i), callback=self.parse,
                                 errback=self.on_error,
                                 dont_filter=True)

    def on_error(self, failure):
        self.logger.error(repr(failure))

    def parse(self, response):
        rows = response.css("tbody tr")
        content = [["date", "meeting_title", "category", "URL"]]

        # Loop through each <tr> row in the table
        for row in rows:
            date = row.css("td.views-field-field-calendar-date span.date-display-single::text").get()
            title = row.css("td.views-field-title::text").get().replace("\r\n            ", "").replace("          ", "")
            content += self.parse_documents(date, title, row.css("td.views-field-field-agendas div ul li"), self.get_agenda_category)
            content += self.parse_documents(date, title, row.css("td.views-field-field-packets a"), self.get_packet_category)
            content += self.parse_documents(date, title, row.css("td.views-field-field-minutes div ul li"), self.get_minutes_category)

        self.save_to_csv(content)

    def get_agenda_category(self, link_text) -> str:
        return "agenda" if link_text is None or "agenda" in link_text.lower() else "other"

    def get_packet_category(self, link_text) -> str:
        return "agenda_packet" if link_text is None or "packet" == link_text.lower() or "amended" in link_text.lower() else "other"

    def get_minutes_category(self, link_text) -> str:
        return "minutes" if link_text is None or "minutes" == link_text.lower() else "other"

    def parse_documents(self, date, title, documents, category_function) -> []:
        document_data = []
        for document in documents:
            category = document.css("a::text").get()  # Link text
            category = category_function(category)
            url = document.css("a").attrib["href"]
            document_data.append([date, title, category, url])
        return document_data

    # Generate a timestamp for the filename
    def generate_timestamp(self) -> str:
        return datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S.%f")

    # Save data to csv file
    def save_to_csv(self, contents):
        file_name = "CO_LINCOLN_WI_US_MEETINGS-metadata-" + self.generate_timestamp() + ".csv"
        try:
            with open(file_name, 'w', newline='') as file:
                writer = csv.writer(file)
                for i in range(len(contents)):
                    writer.writerow(contents[i])
        except Exception as e:
            print(e)

