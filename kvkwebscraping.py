#!/usr/bin/python

from bs4 import BeautifulSoup
from urllib2 import urlopen
from urllib import urlencode
import re
import json
import sys, getopt

def create_filter_url(filter, page):
    start = page * 10
    keyvalue_pairs = [('handelsnaam', filter["handelsnaam"]), ('kvknummer', filter["kvknummer"]), ('straat', filter["straat"]), ('postcode', filter["postcode"]), ('huisnummer', filter["huisnummer"]), ('plaats', filter["plaats"])]
    return "http://zoeken.kvk.nl/search.ashx?callback=jQuery110204350354116406624_1411845642855&" + \
    urlencode(keyvalue_pairs) + "&hoofdvestiging=true&rechtspersoon=true&nevenvestiging=true&zoekvervallen=0&zoekuitgeschreven=1&start=" + str(start) + "&initial=0&searchfield=uitgebreidzoeken&_=1411845642860"

def output_to_file(filename, data):
    file = open(filename, "w")
    if type(data) is str:
        file.write(data)
    else:
        file.write(data.prettify("utf-8"))

def has_hoofdvestiging_tag(search_result):
    result = search_result.find("a", class_="hoofdvestigingTag")
    if result is None:
        return False
    else:
        return True

def retrieve_aantal_resultaten(searchpage):
    aantal = 0
    feedback = searchpage.find("div", class_="feedback")
    if feedback is not None:
        aantal = feedback.text[0 : feedback.text.find(" ")]
    return int(aantal)

def calc_aantal_paginas(aantal_resultaten):
    rest = aantal_resultaten % 10
    if rest > 0:
        add_page = 1
    else:
        add_page = 0
    return (aantal_resultaten / 10) + add_page

def retrieve_kvk_meta(kvk_meta):
    result = ""
    for li in kvk_meta.find_all("li"):
        if li.string is not None:
            value = li.string.strip()
            if (len(value) > 0):
                if (result <> ""):
                    result = result + ", "
                result = result + value
    return result        

def retrieve_handelsnamen(handelsnamen, searchpage):
    for li in searchpage.find_all("li", class_="type1"):
        handelsnaam = li.find("h3", class_="handelsnaamHeader")
        kvk_meta = retrieve_kvk_meta(li.find("ul", class_="kvk-meta"))
        hoofdvestiging = ""
        if (has_hoofdvestiging_tag(li)):
            hoofdvestiging = "Hoofdvestiging, "
        handelsnamen.append(handelsnaam.a.string + " [" + hoofdvestiging + kvk_meta + "]")
    return handelsnamen

def load_searchpage(search_url):
    request = urlopen(search_url)
    response = request.read()
    json_encoded = response[response.find("(") + 1 : response.find(");")]
    json_encoded = json_encoded.replace("\t", " ")
#    json_encoded = re.sub(r'(?<=>)(.*)(\\)(.*)(?=<)', r'\1\\\2\3', json_encoded)
    try:
        json_decoded = json.loads(json_encoded)
    except ValueError as e:
        output_to_file("response.html", response)
        output_to_file("encoded.json", json_encoded)
        raise Exception("Error decoding json, check html_respons.html and encoded.json [" + str(e) + "]")
    else:
        soup = BeautifulSoup(json_decoded["html"])
        searchpage = soup.find("div", class_="searchpage")
        if searchpage is None:
            raise "Search page not found"
        return searchpage

def init(search_url):
    searchpage = load_searchpage(search_url)
    search_results = {}
    search_results["results"] = retrieve_aantal_resultaten(searchpage)
    search_results["pages"] = calc_aantal_paginas(search_results["results"])
    return search_results 

def search(filter, max_results):
    max_pages = (max_results - (max_results % 10)) / 10
    search_results = init(create_filter_url(filter, 0))
    print "Aantal resultaten: %s [aantal pagina's: %s, max pages: %s]" % (str(search_results["results"]), str(search_results["pages"]), max_pages)
    handelsnamen = []
    handelsnamen.append("Aantal resultaten: " + str(search_results["results"]) + " [aantal pagina's: " + str(search_results["pages"]) + "]")
    if search_results["pages"] < max_pages:
        max_pages = search_results["pages"]
    for page in range(0, max_pages):
        if page % 10 == 0:
            print "Pages read: %s" % page
        searchpage = load_searchpage(create_filter_url(filter, page))
        handelsnamen = retrieve_handelsnamen(handelsnamen, searchpage)
    return handelsnamen

def help_message():
    print "webscraping101.py -n <handelsnaam> -p <plaats> -m <maxresults>"

def main(argv):
    handelsnaam = ""
    plaats = ""
    max_results = 100

    try:
        opts, args = getopt.getopt(argv, "hn:p:m:", ["handelsnaam=", "plaats=", "max_results="])
    except getopt.GetoptError, exec_error:
        print exec_error
        help_message()
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            help_message()
            sys.exit()
        elif opt in ("-n", "--handelsnaam"):
            handelsnaam = arg
        elif opt in ("-p", "--plaats"):
            plaats = arg
        elif opt in ("-m", "--max_results"):
            max_results = int(arg)
    if (handelsnaam == "") and (plaats == ""):
        print "Error: no parameters specified"
        help_message()
        sys.exit(2)

    filter = {}
    filter["handelsnaam"] = handelsnaam
    filter["kvknummer"] = ""
    filter["straat"] = ""
    filter["huisnummer"] = ""
    filter["postcode"] = ""
    filter["plaats"] = plaats

    print "max_results=%s" % max_results
    handelsnamen = search(filter, max_results)

    if handelsnamen is not None:
        for handelsnaam in handelsnamen:
            print handelsnaam
            print ("Ingelezen resultaten: %s") % len(handelsnamen)

if __name__ == "__main__":
    main(sys.argv[1:])
