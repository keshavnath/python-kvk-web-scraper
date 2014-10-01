#!/usr/bin/python

from bs4 import BeautifulSoup
from multiprocessing import Pool as ThreadPool
from urllib2 import urlopen
from urllib import urlencode
import json
import pprint
import re
import sys, getopt
import time

# Increase recursion limit (stack depth)
sys.setrecursionlimit(10000)

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

def retrieve_kvk_meta(organisatie, kvk_meta):
    adres = {}
    adres_cnt = 0
    adres_fields = ( "straat", "postcode", "plaats" )
    organisatie["adres"] = adres
    for li in kvk_meta.find_all("li"):
        if li.string is not None:
            value = li.string.strip()
            if (len(value) > 0):
                if (value == ""):
                    continue
                elif (value.startswith("KVK")):
                    organisatie["kvk_nummer"] = value[4:]
                elif (value.startswith("Vestigingsnr.")):
                    organisatie["vestigingsnr"] = value[14:]
                elif (value.startswith("Nevenvestiging")):
                    organisatie["nevenvestiging"] = "ja"
                elif (value.startswith("Rechtspersoon")):
                    organisatie["nevenvestiging"] = "ja"
                else:
                    if (adres_cnt > len(adres_fields) - 1):
                        print "Error: unknown value found after address [%s]" % value
                    adres[adres_fields[adres_cnt]] = value
                    adres_cnt += 1

def retrieve_organisaties(organisaties, searchpage):
    for li in searchpage.find_all("li", class_="type1"):
        organisatie = {}
        handelsnaam = li.find("h3", class_="handelsnaamHeader")
        organisatie["handelsnaam"] = handelsnaam.a.string
        retrieve_kvk_meta(organisatie, li.find("ul", class_="kvk-meta"))
        if (has_hoofdvestiging_tag(li)):
            organisatie["hoofdvestiging"] = "Hoofdvestiging, "
        organisaties.append(organisatie)
    return organisaties 

def load_searchpage(search_url):
    request = urlopen(search_url)
    response = request.read()
    json_encoded = response[response.find("(") + 1 : response.find(");")]
    json_encoded = json_encoded.replace("\t", " ")
    #json_encoded = re.sub(r'(?<=<.*>)(.*)(\\)(.*)(?=</.*>)', r'\1\\\2\3', json_encoded)
    try:
        json_decoded = json.loads(json_encoded)
    except ValueError as e:
        output_to_file("response.html", response)
        output_to_file("encoded.json", json_encoded)
        raise Exception("Error decoding json, check html_respons.html and encoded.json [" + str(e) + "]")
    else:
        soup = BeautifulSoup(json_decoded["html"], "lxml")
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

def process_search(search_url):
    organisaties = []
    searchpage = load_searchpage(search_url)
    retrieve_organisaties(organisaties, searchpage)
    return organisaties

def search(filter, max_results):
    start_time = time.time()

    if max_results > -1:
        max_pages = (max_results - (max_results % 10)) / 10
    else:
        max_pages = -1
    
    search_results = init(create_filter_url(filter, 0))
    resultaten= {}
    resultaten["stats"] = ("Aantal resultaten: " + str(search_results["results"]) + " [aantal pagina's: " + str(search_results["pages"]) + "]")
    
    if search_results["pages"] < max_pages or max_pages == -1:
        max_pages = search_results["pages"]
    
    # Create list of search urls
    search_urls = []
    for page in range(0, max_pages):
        search_urls.append(create_filter_url(filter, page))
    
    # Create pool of worker threads
    pool = ThreadPool(4)
    # Open the urls in their own threads
    organisaties = pool.map(process_search, search_urls)
    pool.close()
    pool.join()

    # Make a single organisation array
    new_organisaties = []
    for i in range(0, len(organisaties)):
        new_organisaties = new_organisaties + organisaties[i]
    resultaten["organisaties"] = new_organisaties
    resultaten["exectime"] = time.time() - start_time
    
    return resultaten

def help_message():
    print "webscraping101.py -n <handelsnaam> -p <plaats> -m <maxresults>"

def main(argv):
    handelsnaam = ""
    plaats = ""
    max_results = -1

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
    print ""

    resultaten = search(filter, max_results)
    organisaties = resultaten["organisaties"]
    
    pp = pprint.PrettyPrinter(indent=4)
    #pp.pprint(resultaten)
    
    if organisaties is not None:
        for organisatie in organisaties:
            print organisatie["handelsnaam"] + " [" + organisatie["kvk_nummer"]+ "]"
   
    print "" 
    print resultaten["stats"]
    print "Ingelezen resultaten: %s" % len(organisaties)
    print "Exectime: %s ms" % resultaten["exectime"]

if __name__ == "__main__":
    main(sys.argv[1:])
