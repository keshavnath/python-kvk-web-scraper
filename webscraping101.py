#!/usr/bin/python

from bs4 import BeautifulSoup
from urllib2 import urlopen

BASE_URL = "http://www.chicagoreader.com"

def get_headline_links(section_url):
    html_doc = urlopen(section_url).read()
    soup = BeautifulSoup(html_doc)
    bleaderteaser = soup.find("div", id="BleaderTeaser")
    print bleaderteaser
    headline_links = [li.a["href"] for li in bleaderteaser.find_all("li")]
    return headline_links

links = get_headline_links("http://www.chicagoreader.com/chicago/food-and-drink/Section?oid=846971")
print len(links)
for link in links:
    print link
