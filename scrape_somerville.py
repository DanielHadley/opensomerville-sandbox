import csv
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

sville_base = 'http://somervillecityma.iqm2.com/Citizens/'
sville_main = sville_base + 'Calendar.aspx'

def parse_url(url):
    s=scrapelib.Scraper()
    data = s.urlopen(url)
    parse_data(data)

def parse_data(data):
    rows = parse_calendar(data)
    with open('attendance.csv', 'wb') as out:
        writer = csv.writer(out)
        headers = 'date board type name title status'.split()
        writer.writerow(headers)
        for raw_desc, minutes_url in rows:
            if not minutes_url:
                continue
            
            desc = parse_description(raw_desc)
            print desc
            minutes = get_minutes_as_text(sville_base + minutes_url)
            attendance = find_attendance(minutes)
            for attend in attendance:
                row = desc + attend
                writer.writerow(row)
        

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
    valid_statuses = set(['Present', 'Absent', 'Excused', 'Remote'])
    
    result = []
    lines = iter(data.splitlines())
    for line in lines:
        if 'Attendee Name' in line:
            break
            
    for line in lines:
        line = line.strip()
        if not line:
            break   # End of the attendance section
                    # assuming it doesn't span a page break...
        fields = re.split('\s\s+', line)
        if len(fields) < 2 or fields[-1] not in valid_statuses:
            break   # Bad data, assume that is the end
            
        if len(fields) == 3:
            result.append(tuple(fields))
        else:
            result.append((fields[0], '', fields[1]))
    return result
    
def find_status(fields):
    """ Find the attendance status in a list of fields.
        We don't know which field it is, there may be one missing. """
    statuses = ['Present', 'Absent', 'Excused', 'Remote']
    for field in fields:
        if field in statuses:
            return field
    print "Can't find status in", fields
    return 'Unknown'
    
if __name__ == '__main__':
    if len(sys.argv) > 1:
        url = sys.argv[1]
        parse_url(url)

