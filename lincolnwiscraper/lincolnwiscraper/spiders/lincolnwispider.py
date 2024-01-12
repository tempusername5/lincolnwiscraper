import scrapy

class LincolnwispiderSpider(scrapy.Spider):
    name = "lincolnwispider"
    allowed_domains = ["co.lincoln.wi.us"]
    start_url = "https://co.lincoln.wi.us/meetings"

    # Allow an additional argument for number of pages
    # This can be entered when calling the scrapy crawl command with the -a flag. For example:
    # scrapy crawl lincolnwispider -a total_pages=2
    def __init__(self, total_pages=2, **kwargs):
        self.total_pages = total_pages
        super().__init__(**kwargs)

    # Parse each page, up to total_pages defined in the constructor
    # Page numbering for this website is 0-based so page 1 uses ?page=0
    def start_requests(self):
        for i in range(int(self.total_pages)):
            yield scrapy.Request(self.start_url + "?page=" + str(i), callback=self.parse,
                                 errback=self.on_error,
                                 dont_filter=True)

    # Parse the contents of the webpage and output the contents
    # -O flag should be used to save the output into a JSON or CSV file
    def parse(self, response):
        rows = response.css("tbody tr")

        # List of pairs 1.paths for cell element (agenda, packet, minute cells) 2.function to categorize document
        cells = [
            {"element_path": "td.views-field-field-agendas div ul li", "type": "agenda", "keyword": "agenda"},
            {"element_path": "td.views-field-field-packets a", "type": "agenda_packet", "keyword": "packet"},
            {"element_path": "td.views-field-field-minutes div ul li", "type": "minutes", "keyword": "minutes"}
        ]

        # Loop through each <tr> row in the table
        for row in rows:
            date = self.get_date(row)
            title = self.get_title(row)

            # Loop through each cell in the table
            for cell in cells:
                element = row.css(cell["element_path"])

                # Loop through each <li> or <a> list for each type of cell (agenda, packet, minute)
                for li in element:
                    category = li.css("a::text").get()  # Get link text
                    category = self.get_category(category, cell["type"], cell["keyword"])  # Change category based on link text
                    url = li.css("a").attrib["href"]  # Get document link
                    yield {"date": date, "meeting_title": title, "category": category, "URL": url}  # Output contents as one line in the csv file

    # Error callback. Will be called if scrapy encounters errors with the request
    def on_error(self, failure):
        self.logger.error(repr(failure))

    # Grab the date from the date cell in the table
    # "Content" attribute is in the format 2023-11-13T13:00:00-06:00, only YYYY-MM-DD is grabbed
    def get_date(self, element):
        return element.css("td.views-field-field-calendar-date span.date-display-single").attrib["content"][:10]

    # Grab the meeting title from the table and remove extraneous spacing
    def get_title(self, element):
        return element.css("td.views-field-title::text").get().replace("\r\n            ", "").replace("          ", "")

    # Documents will be categorized as the specified document_type if they contain any of:
    # the specified keyword, "amended", "revised", "cancel", or "corrected"
    # Otherwise they will be categorized as "other"
    def get_category(self, link_text, document_type, keyword) -> str:
        if link_text is not None:
            link_text = link_text.lower()
        return document_type if (link_text is None or
                                 keyword == link_text or
                                 "amended" in link_text or
                                 "revised" in link_text or
                                 "cancel" in link_text or
                                 "corrected" in link_text) else "other"
