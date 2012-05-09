"""
scraper_test.py

Created by Kent Johnson on 2012-04-28.
"""

import unittest
from datetime import datetime

from scrape_somerville import find_attendance, parse_calendar, parse_description

class ScraperTest(unittest.TestCase):
    first_description = """THURSDAY, APRIL 26, 2012  7:00 PM

Board:\tBoard of Aldermen
Type:\tRegular Meeting
Status:\tScheduled

\tAldermanic Chambers
\tCity Hall, 93 Highland Avenue, Somerville, MA  02143"""
    
    attendance_text = '''
    
    Attendee Name                                 Title                Status       Arrived
    William A. White Jr.          Chair                              Present
    Tony Lafuente                 Vice Chair                         Present
    Sean T. O'Donovan             Ward Five Alderman                 Absent
    Omar Boukili                  Administrative Assistant           Excused
    George Proakis                Director of Planning               Remote
    Brad Ross                                                        Present
    Dennis M. Sullivan            Alderman At Large                  Present
'''

    def setUp(self):
        pass

    def test_parser(self):
        data = open('test_data/Calendar.html').read()
        actual = parse_calendar(data)
        self.assertEquals(len(actual), 73)
        self.assertEquals(actual[0][0], self.first_description)
        self.assertEquals(actual[0][1], '')
        self.assertEquals(actual[6][1], 'FileOpen.aspx?Type=15&ID=1327')
    
    def test_parse_description(self):
        data = parse_description(self.first_description)
        self.assertEquals(data.date, datetime(2012, 4, 26, 19, 0))
        self.assertEquals(data.board, 'Board of Aldermen')
        self.assertEqual(data.type, 'Regular Meeting')
    
    def test_find_attendance(self):
        data = find_attendance(self.attendance_text)
        self.assertEquals(len(data), 7)
        self.assertEquals(data[0], ['William A. White Jr.', 'Chair', 'Present'])
        self.assertEquals(data[2][2], 'Absent')
        self.assertEquals(data[3][2], 'Excused')
        self.assertEquals(data[4][2], 'Remote')
        self.assertEquals(data[5], ('Brad Ross', '', 'Present'))
        
if __name__ == '__main__':
    unittest.main()
    