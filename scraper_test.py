"""
scraper_test.py

Created by Kent Johnson on 2012-04-28.
"""

import unittest
from datetime import datetime

from scrape_somerville import parse_calendar, parse_description

class ScraperTest(unittest.TestCase):
    first_description = """THURSDAY, APRIL 26, 2012  7:00 PM

Board:\tBoard of Aldermen
Type:\tRegular Meeting
Status:\tScheduled

\tAldermanic Chambers
\tCity Hall, 93 Highland Avenue, Somerville, MA  02143"""
    
    def setUp(self):
        pass

    def testParser(self):
        data = open('Calendar.html').read()
        actual = parse_calendar(data)
        self.assertEquals(len(actual), 73)
        self.assertEquals(actual[0][0], self.first_description)
        self.assertEquals(actual[0][1], '')
        self.assertEquals(actual[6][1], 'FileOpen.aspx?Type=15&ID=1327')
    
    def testParseDescription(self):
        data = parse_description(self.first_description)
        self.assertEquals(data.date, datetime(2012, 4, 26, 19, 0))
        self.assertEquals(data.board, 'Board of Aldermen')
        self.assertEqual(data.type, 'Regular Meeting')
if __name__ == '__main__':
    unittest.main()
    