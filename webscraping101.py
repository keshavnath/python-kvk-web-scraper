#!/usr/bin/python

from bs4 import BeautifulSoup
from urllib2 import urlopen

BASE_URL = "http://www.nu.nl"

def get_headline_links(section_url):
    html_doc = urlopen(section_url).read()
    soup = BeautifulSoup(html_doc)
    section_algemeen = soup.find("div", class_="section algemeen")
    if section_algemeen is None:
        print "Section not found [section algemeen]"
    else:
        headline_links = [BASE_URL + li.a["href"] for li in section_algemeen.find_all("li")]
        lead_article = section_algemeen.find("div", class_="leadarticle")
        headline_links.insert(0, BASE_URL + lead_article.h3.a["href"]) 
        return headline_links

links = get_headline_links(BASE_URL)

if links is not None:
    for link in links:
        print link
