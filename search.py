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
    search_url = None

    def __init__(self, filter, startpage, maxpages):
        self.filter = filter
        self.startpage = startpage
        self.maxpages = maxpages
        
        filter = Filter(self.filter, self.startpage, self.maxpages)
        self.search_url = filter.create_filter_url(self.startpage)
        handler = Handler(self.search_url)
        self.search_results = handler.init()
      
        if self.search_results["pages"] < startpage: 
            raise Exception("Error: startpage exceeds available pages [pages=" + str(self.search_results["pages"]) + "]")
        if self.search_results["pages"] < startpage + maxpages:
            self.maxpages = self.search_results["pages"]

    def get_search_url(self):
        return self.search_url

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
        results["organisaties"] = self.consolidate(organisaties)
        
        timer.stop()
        
        results["stats"] = [ { "exectime": timer.exectime(), "matches": { "total": str(self.search_results["results"]), "pages": str(self.search_results["pages"]) }, "read": { "page_from": str(self.startpage), "page_to": str(self.maxpages) + "]" } } ]
        
        return results
