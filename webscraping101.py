#!/usr/bin/python

from bs4 import BeautifulSoup
from urllib2 import urlopen
from urllib import urlencode
import json
import sys, getopt

def create_search_url(handelsnaam, kvknummer, straat, postcode, huisnummer, plaats):
    keyvalue_pairs = [('handelsnaam', handelsnaam), ('kvknummer', kvknummer), ('straat', straat), ('postcode', postcode), ('huisnummer', huisnummer), ('plaats', plaats)]
    return "http://zoeken.kvk.nl/search.ashx?callback=jQuery110204350354116406624_1411845642855&" + \
    urlencode(keyvalue_pairs) + "&hoofdvestiging=true&rechtspersoon=true&nevenvestiging=true&zoekvervallen=0&zoekuitgeschreven=1&start=0&initial=0&searchfield=uitgebreidzoeken&_=1411845642860"

def output_to_file(filename, soup):
    file = open(filename, "w")
    file.write(soup.prettify("utf-8"))

def has_hoofdvestiging_tag(search_result):
    result = search_result.find("a", class_="hoofdvestigingTag")
    if result is None:
        return False
    else:
        return True

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

def retrieve_handelsnamen(searchpage):
    handelsnamen = []
    for li in searchpage.find_all("li", class_="type1"):
        handelsnaam = li.find("h3", class_="handelsnaamHeader")
        kvk_meta = retrieve_kvk_meta(li.find("ul", class_="kvk-meta"))
        hoofdvestiging = ""
        if (has_hoofdvestiging_tag(li)):
            hoofdvestiging = "Hoofdvestiging, "
        handelsnamen.append(handelsnaam.a.string + " [" + hoofdvestiging + kvk_meta + "]")
    return handelsnamen

def get_headline_links(search_url):
    html_respons = urlopen(search_url).read()
    json_encoded = html_respons[html_respons.find("(") + 1 : html_respons.find(")")]
    json_decoded = json.loads(json_encoded.replace("\t", "  "))
    soup = BeautifulSoup(json_decoded["html"])
    output_to_file("complete.html", soup)
    searchpage = soup.find("div", class_="searchpage")
    if searchpage is None:
        print "Search page not found"
        handelsnamen = []
    else:
        handelsnamen = retrieve_handelsnamen(searchpage)
    return handelsnamen

def help_message():
    print "webscraping101.py -n <handelsnaam> -p <plaats>"

def main(argv):
    handelsnaam = ""
    plaats = ""
    try:
        opts, args = getopt.getopt(argv, "hn:p:", ["handelsnaam=", "plaats="])
    except getopt.GetoptError:
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
    if (handelsnaam == "") and (plaats == ""):
        print "Error: no parameters specified"
        help_message()
        sys.exit(2)

    handelsnamen = get_headline_links(create_search_url(handelsnaam, "", "", "", "", plaats))
    if handelsnamen is not None:
        for handelsnaam in handelsnamen:
            print handelsnaam

if __name__ == "__main__":
    main(sys.argv[1:])
