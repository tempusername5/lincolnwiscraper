import unittest
from lincolnwispider import LincolnwispiderSpider
import os
from scrapy.http import Response, Request

import requests
from scrapy.http import HtmlResponse
class MyTestCase(unittest.TestCase):
    # Test that passing a parameter to the spider actually affects the total_pages
    def test_constructor_argument(self):
        self.assertEqual(LincolnwispiderSpider(10).total_pages, 10)

    # Test the parsing function of the spider
    # This test just counts the number of rows and checks that no fields are empty
    def test_parse(self):
        # Create a request from the test HTML page
        file_name = 'test.html'
        url = 'http://www.example.com'
        request = Request(url=url)

        file_content = open(file_name, 'r').read()
        response = HtmlResponse(url=url,
                            request=request,
                            body=file_content, encoding = 'utf-8')
        results = LincolnwispiderSpider().parse(response)

        # Count each row, make sure no fields are empty
        count = 0
        for item in results:
            count += 1
            self.assertIsNotNone(item['date'])
            self.assertIsNotNone(item['meeting_title'])
            self.assertIsNotNone(item['category'])
            self.assertIsNotNone(item['URL'])
        self.assertEqual(count, 125)

if __name__ == '__main__':
    unittest.main()
