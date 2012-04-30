import sys
import os
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
    lines = description.splitlines()
    date = datetime.strptime(lines[0], '%A, %B %d, %Y %I:%M %p')
    board = lines[2].split(None, 1)[1]
    type_ = lines[3].split(None, 1)[1]
    return MeetingRecord(date, board, type_)
    
if __name__ == '__main__':
	main()

