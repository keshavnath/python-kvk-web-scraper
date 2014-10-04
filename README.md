# KvKWebScraper

This is a service implemented in Python that provides an api to search for 
organisations in the database of the Dutch Chamber of Commerce (KvK). It uses web scraping
to extract the information from the search functionality of the KvK website.

## Disclaimer / notes of caution

I have just started programming in Python. For a previous project I implemented
simalar functionality using Java. I thought it would be a good excercise to 
reimplement using Python.

If you have any suggetions or improvements please let me know.

This code has only been test under Linux Mint 17.

## Limitations

* **Terminated organisations** - Currently organisations that have been 
  terminated are not searched.

* **Search options** - Search options are limited to 'handelsnaam' and
  'plaats'.

## Features

* **Search options** - The following search options are supported: 'handelsnaam'
  and 'plaats'.

* **Paging** - Paging is supported. It is possible to specify the starting
  page and number of pages to read.

* **REST/JSON** - A REST/JSON API is supported.
  
* **Command line tool** - The functionality can also be used from the command line.

## Future improvements

* **Terminated organisations** - Add an option to search for terminated organisations.

* **Search options** - Support all extended search options.

* **Simple GUI** - Add a simpel web GUI as front-end.

* **Improve command line** - Command line is very basis, enhance response.

* **Sorting** - Sort the results. For this to work correctly caching will need to
  be implemented.

* **Testing** - Add unit testing.

## Prerequisites

The following prerequisites must be fulfilled:

- Python 2.7 or later (sudo apt-get install python2.7)
- Flask microframework (pip install Flask)
- BeautifulSoup library (pip install beautifulsoup4)
- lxlm library (pip install lxml)

## Quick start

The web scraper can be used as command line tool or service.

**Command line tool**

```
./kvkwebscraper.py -n Test
```

**Service**

Start the Flask microframework:

```
./service.py
```

Call the service:

```
curl -i http://127.0.0.1:5000/v1/organisations?plaats=Mijnsheerenland&maxpages=2
```
