#!/usr/bin/python

import argparse
import logger_init
import logging
import sys
from search import Search
from timer import Timer
from handler import NoResultsError

release = "0.7.0"

logger = logging.getLogger("webscraper_app.kvkwebscraper")

def help_message():
    print "kvkwebscraping.py -n <handelsnaam> -p <plaats> -s <startpage> -m <maxpages>"

def parse_args():
    parser = argparse.ArgumentParser(description="Web scraping of the KvK search functionality [version " + str(release) + "]")

    parser.add_argument("-a", "--handelsnaam", metavar="handelsnaam", default="", help="name or partial name of an organisation to search for")
    parser.add_argument("-k", "--kvknummer", metavar="kvknummer", default="", help="KvK number to limit the search to")
    parser.add_argument("-t", "--straat", metavar="straat", default="", help="streat to limit the search to")
    parser.add_argument("-i", "--huisnummer", metavar="huisnummer", default="", help="house number to limit the search to")
    parser.add_argument("-z", "--postcode", metavar="postcode", default="", help="zipcode to limit the search to")
    parser.add_argument("-p", "--plaats", metavar="plaats", default="", help="city to limit the search to")
    parser.add_argument("-s", "--startpage", metavar="startpage", type=int, default=1, help="page to start processing from")
    parser.add_argument("-m", "--maxpages", metavar="maxpages", type=int, default=1, help="maximum number of pages to return")
    parser.add_argument("-o", "--hoofdvestiging", metavar="hoofdvestiging", type=bool, default=True, help="select 'hoofdvestigingen'")
    parser.add_argument("-n", "--nevenvestiging", metavar="nevenvestiging", type=bool, default=True, help="select 'nevenvestigingen'")
    parser.add_argument("-r", "--rechtspersoon", metavar="rechtspersoon", type=bool, default=True, help="select 'rechtspersonen'")
    parser.add_argument("-v", "--vervallen", metavar="vervallen", type=bool, default=False, help="select 'vervallen handelsnamen'")
    parser.add_argument("-u", "--uitgeschreven", metavar="uitgeschreven", type=bool, default=False, help="select 'uitgeschreven vestigingen en rechtspersonen (na 1 januari 2012)'")

    args = parser.parse_args()

    if args.handelsnaam == "" and args.kvknummer == "" and args.straat == "" and args.huisnummer == "" and args.postcode == "" and args.plaats == "":
        print "error: handelsnaam, kvknummer, straat, huisnummer, postcode or plaats must be specified\n"
        parser.print_help()
        sys.exit(2)
        
    return args

def main(args):
    timer = Timer()
    timer.start()
            
    filter = {}
    filter["handelsnaam"] = args.handelsnaam
    filter["kvknummer"] = args.kvknummer
    filter["straat"] = args.straat
    filter["huisnummer"] = args.huisnummer
    filter["postcode"] = args.postcode
    filter["plaats"] = args.plaats
    filter["hoofdvestiging"] = "true" if args.hoofdvestiging == True else "false"
    filter["nevenvestiging"] = "true" if args.nevenvestiging == True else "false"
    filter["rechtspersoon"] = "true" if args.rechtspersoon == True else "false"
    filter["vervallen"] = "1" if args.vervallen == True else "0"
    filter["uitgeschreven"] = "1" if args.uitgeschreven == True else "0"

    logger.debug(filter)

    try:
        search = Search(filter, args.startpage, args.maxpages)
        results = search.run()
    except NoResultsError:
        print "Error: no results found"
        sys.exit(1)

    organisations = results["organisaties"]
    
    if organisations is not None:
        for organisation in organisations:
            print organisation["handelsnaam"] + " [" + organisation["kvk_nummer"]+ "]"
   
    print "" 
    stats = results["stats"]
    print "Gevonden: resultaten=%s, pagina's=%s" % (stats["matches"]["total"], stats["matches"]["pages"])
    print "Ingelezen pagina: van=%s, tot=%s" % (stats["read"]["page_from"], stats["read"]["page_to"])
    
    timer.stop()
        
    print "Exectime: totaal=%s ms, verwerken=%s ms" % (timer.exectime(), stats["exectime"])

if __name__ == "__main__":
    main(parse_args())
