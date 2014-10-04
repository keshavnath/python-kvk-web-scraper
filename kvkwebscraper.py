#!/usr/bin/python

import argparse
import logger_init
import sys
from search import Search
from timer import Timer

release = "0.5.0"

def help_message():
    print "kvkwebscraping.py -n <handelsnaam> -p <plaats> -s <startpage> -m <maxpages>"

def parse_args():
    parser = argparse.ArgumentParser(description="Web scraping of the KvK search functionality [version " + str(release) + "]")

    parser.add_argument("-n", "--handelsnaam", metavar="handelsnaam", default="", help="name or partial name of an organisation to search for")
    parser.add_argument("-p", "--plaats", metavar="plaats", default="", help="city to limit the search to")
    parser.add_argument("-s", "--startpage", metavar="startpage", type=int, default=1, help="page to start processing from")
    parser.add_argument("-m", "--maxpages", metavar="maxpages", type=int, default=1, help="maximum number of pages to return")

    args = parser.parse_args()

    if args.handelsnaam == "" and args.plaats == "":
        print "error: handelsnaam or plaats must be specified\n"
        parser.print_help()
        sys.exit(2)
        
    return args

def main(args):
    timer = Timer()
    timer.start()
            
    filter = {}
    filter["handelsnaam"] = args.handelsnaam
    filter["kvknummer"] = ""
    filter["straat"] = ""
    filter["huisnummer"] = ""
    filter["postcode"] = ""
    filter["plaats"] = args.plaats

    search = Search(filter, args.startpage, args.maxpages)
    results = search.run()
    organisations = results["organisaties"]
    
    if organisations is not None:
        for organisation in organisations:
            print organisation["handelsnaam"] + " [" + organisation["kvk_nummer"]+ "]"
   
    print "" 
    print results["stats"]
    print "Ingelezen resultaten: %s" % len(organisations)
    print "Exectime: %s ms" % results["exectime"]
    
    timer.stop()
        
    print "Total exectime: %s ms" % timer.exectime()

if __name__ == "__main__":
    main(parse_args())
