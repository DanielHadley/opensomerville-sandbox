import sys
import os
import urllib

import scrapelib
from lxml import etree

sville_main = 'http://somervillecityma.iqm2.com/Citizens/Calendar.aspx'

def main():
	s=scrapelib.Scraper()
	#data = s.urlopen(sville_main)
	data = open('Calendar.html').read()
	tree = etree.HTML(data)
	
	rows = tree.xpath("//div[@class='RowTop']")	
	for row in rows:
		anchors = row.xpath('.//a')
		# First anchor has meeting info in the title attribute
		print anchors[0].attrib['title'].replace('\r', '\n')
		
		# Look for a link to minutes
		minutes = None
		for a in anchors:
			if a.text == 'Minutes':
				minutes = a.attrib['href']
		if minutes:
			print 'Minutes:', minutes
		print
			
if __name__ == '__main__':
	main()

