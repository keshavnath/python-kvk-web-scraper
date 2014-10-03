#!/usr/bin/python

import getopt
import pprint
import sys
from search import Search
from timer import Timer

def help_message():
    print "webscraping101.py -n <handelsnaam> -p <plaats> -s <startpage> -m <maxpages>"

def main(argv):
    timer = Timer()
    timer.start()
            
    handelsnaam = ""
    plaats = ""
    startpage = 1
    maxpages = 1

    try:
        opts, args = getopt.getopt(argv, "hn:p:s:m:", ["handelsnaam=", "plaats=", "startpage", "maxpages="])
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
        elif opt in ("-s", "--startpage"):
            startpage = int(arg)
        elif opt in ("-m", "--maxpages"):
            maxpages = int(arg)
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

    search = Search(filter, startpage, maxpages)
    results = search.run()
    organisations = results["organisaties"]
    
    pp = pprint.PrettyPrinter(indent=4)
    #pp.pprint(resultaten)
    
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
    main(sys.argv[1:])