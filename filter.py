#!/usr/bin/python

from urllib import urlencode

class Filter:
    'Create search filter for the KvK website search functionality'
    filter = ""
    startpage = 1
    maxpages = 1

    def __init__(self, filter, startpage, maxpages):
        self.filter = filter
        self.startpage = startpage
        self.maxpage = maxpages

    def create_filter_url(self, page):
        keyvalue_pairs = [('handelsnaam', self.filter["handelsnaam"]), ('kvknummer', self.filter["kvknummer"]), ('straat', self.filter["straat"]), ('postcode', self.filter["postcode"]), ('huisnummer', self.filter["huisnummer"]), ('plaats', self.filter["plaats"])] 
        return "http://zoeken.kvk.nl/search.ashx?callback=jQuery110204350354116406624_1411845642855&" + \
            urlencode(keyvalue_pairs) + "&hoofdvestiging=true&rechtspersoon=true&nevenvestiging=true&zoekvervallen=0&zoekuitgeschreven=1&start=" + \
            str(page) + "&initial=0&searchfield=uitgebreidzoeken&_=1411845642860"