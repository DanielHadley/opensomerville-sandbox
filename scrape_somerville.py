import sys
import os
import urllib

import scrapelib
from lxml import etree

sville_main = 'http://somervillecityma.iqm2.com/Citizens/Default.aspx'

def main():
	s=scrapelib.Scraper()
	data = s.urlopen(sville_main)
	tree = etree.HTML(data)
	
	# The main "Meeting Calendar" table
	table=tree.xpath("//table[@id='table2']//table[@id='table8']")[0]
	
	# The text entries (below the links) are td.MainScreenText
	# The 'title' attribute of the parent tr contains a lot of info, nicely formatted
	rows = table.xpath(".//td[@class='MainScreenText']")
	for row in rows:
		if row.text:
			attrib = row.getparent().attrib
			if 'title' in attrib:
				print attrib['title'].replace('\r', '\n')
				print
			
if __name__ == '__main__':
	main()

