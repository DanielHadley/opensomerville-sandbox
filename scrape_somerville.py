import re
import sys
import os
import subprocess
import tempfile
import urllib

from collections import namedtuple
from datetime import datetime

import scrapelib
from lxml import etree

MeetingRecord = namedtuple('MeetingRecord', 'date board type'.split())

sville_main = 'http://somervillecityma.iqm2.com/Citizens/Calendar.aspx'

def main():
	s=scrapelib.Scraper()
	#data = s.urlopen(sville_main)
	data = open('Calendar.html').read()
	rows = parse_calendar(data)
	for row in rows:
		print parse_description(row[0])

def parse_calendar(data):
	""" Parse a calendar page, return raw descriptions and links to minutes """
	tree = etree.HTML(data)
	
	rows = tree.xpath("//div[@class='RowTop']")	
	result = []
	for row in rows:
		anchors = row.xpath('.//a')
		# First anchor has meeting info in the title attribute
		description = anchors[0].attrib['title'].replace('\r', '\n')
		
		# Look for a link to minutes
		minutes = None
		for a in anchors:
			if a.text == 'Minutes':
				minutes = a.attrib['href']
		result.append((description, minutes))
	return result

def parse_description(description):
    """ Parse the description of a meeting from the 'title' attribute.
        Returns a MeetingRecord with the meeting info. """
    lines = description.splitlines()
    date = datetime.strptime(lines[0], '%A, %B %d, %Y %I:%M %p')
    board = lines[2].split(None, 1)[1]
    type_ = lines[3].split(None, 1)[1]
    return MeetingRecord(date, board, type_)
    
def get_minutes_as_text(url):
    """ Download the minutes of a meeting and convert to text.
        Returns the text of the file. 
        Requires pdftotext for the conversion. """
    s=scrapelib.Scraper()
    data = s.urlopen(url)
    fd, path = tempfile.mkstemp(text=True)
    os.write(fd, data)
    os.close(fd)
    text = subprocess.check_output(['pdftotext', '-layout', '-nopgbrk', path, '-'])
    os.remove(path)
    return text
    
def find_attendance(data):
    """ Find the attendance in the text of minutes.
        Returns pairs of name, attendance for all listed attendees. """
    result = []
    lines = iter(data.splitlines())
    for line in lines:
        if 'Attendee Name' in line:
            for line in lines:
                line = line.strip()
                if not line:
                    return result
                fields = re.split('\s\s+', line)
                result.append((fields[0], fields[2]))
    return result
    
    
if __name__ == '__main__':
	main()

