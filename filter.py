#!/usr/bin/python3

from urllib.parse import urlencode
import logging

class Filter:
    'Create search filter for the KvK website search functionality'
    filter = ""
    startpage = 1
    maxpages = 1
    logger = None

    def __init__(self, filter, startpage, maxpages):
        self.filter = filter
        self.startpage = startpage
        self.maxpage = maxpages
        self.logger = logging.getLogger("webscraper_app.filter")

    def create_filter_url(self, page):
        keyvalue_pairs = [
            ('handelsnaam', self.filter["handelsnaam"]), 
            ('kvknummer', self.filter["kvknummer"]), 
            ('straat', self.filter["straat"]), 
            ('postcode', self.filter["postcode"]), 
            ('huisnummer', self.filter["huisnummer"]), 
            ('plaats', self.filter["plaats"]),
            ('hoofdvestiging', self.filter["hoofdvestiging"]),
            ('rechtspersoon', self.filter["rechtspersoon"]),
            ('nevenvestiging', self.filter["nevenvestiging"]),
            ('zoekvervallen', self.filter["vervallen"]),
            ('zoekuitgeschreven', self.filter["uitgeschreven"])
        ] 
        url = "http://zoeken.kvk.nl/search.ashx?callback=jQuery110204350354116406624_1411845642855&" + \
            urlencode(keyvalue_pairs) + "&start=" + \
            str(page) + "&initial=0&searchfield=uitgebreidzoeken&_=1411845642860"
        self.logger.debug(url)        
        return url
