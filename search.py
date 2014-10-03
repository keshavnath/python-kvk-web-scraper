#!/usr/bin/python

from multiprocessing import Pool as ThreadPool
from timer import Timer
from filter import Filter
from handler import Handler
import sys

# Increase recursion limit (stack depth)
sys.setrecursionlimit(10000)

def unwrap_self_process_search(arg, **kwarg):
    return Search.process_search(*arg, **kwarg)

class Search:
    filter = ""
    startpage = 1
    maxpages = 1
    search_results = None

    def __init__(self, filter, startpage, maxpages):
        self.filter = filter
        self.startpage = startpage
        self.maxpages = maxpages
        
        filter = Filter(self.filter, self.startpage, self.maxpages)
        search_url = filter.create_filter_url(self.startpage)
        handler = Handler(search_url)
        self.search_results = handler.init()
      
        if self.search_results["pages"] < startpage: 
            raise Exception("Error: startpage exceeds available pages [pages=" + str(self.search_results["pages"]) + "]")
        if self.search_results["pages"] < startpage + maxpages:
            maxpages = self.search_results["pages"]

    def process_search(self, search_url):
        organisaties = []
        handler = Handler(search_url)
        searchpage = handler.load_searchpage()
        handler.retrieve_organisaties(organisaties, searchpage)
        return organisaties
    
    def consolidate(self, organisaties):
        new_organisaties = []
        # Make a single organisation array
        for i in range(0, len(organisaties)):
            new_organisaties = new_organisaties + organisaties[i]
        return new_organisaties

    def run(self):
        timer = Timer()
        timer.start()
            
        # Create list of search urls
        search_urls = []
        filter = Filter(self.filter, self.startpage, self.maxpages)
        for page in range(self.startpage, self.startpage + self.maxpages):
            search_urls.append(filter.create_filter_url(page * 10))
        
        # Create pool of worker threads
        pool = ThreadPool(4)
        # Open the urls in their own threads
        organisaties = pool.map(unwrap_self_process_search, zip([self] * len(search_urls), search_urls))
        pool.close()
        pool.join()
    
        results = {}
        results["stats"] = ("Aantal resultaten: " + str(self.search_results["results"]) + " [pagina's: " + str(self.search_results["pages"]) + ", ingelezen: " + str(self.startpage) + "-" + str(self.maxpages) + "]")
        results["organisaties"] = self.consolidate(organisaties)
        
        timer.stop()
        
        results["exectime"] = timer.exectime()
        
        return results