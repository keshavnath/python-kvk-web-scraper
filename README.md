# KvKWebScraper

This is a service provides an api to search for organisations using the search 
functionality of the KvK website (Dutch Chamber of Commerce).

## Disclaimer

I have just started programming in Python. For a previous project I implemented
simalar functionality using Java. I thought it would be a good excercise to 
reimplement using Python.

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

* **REST/JSON** - The API supports REST/API.

* **Command line tool** - The functionality can also be used from the command line.

## Future improvements

* **Terminated organisations** - Add terminated organisations.

* **Search options** - Add additional search options.

* **Simple GUI** - Add a simpel web GUI as front-end.

* **Improve command line** - Command line is very basis, enhance response.

## Prerequisites

The following prerequisites must be fulfilled:

- Python 2.7 or later
- Flask microframework
- BeautifulSOup library
- LXML library

## Quick start

The web scraper can be used as command line tool or service.

**Command line tool**

```
./kvkwebscraper.py -n Test
;;;

**Service**

Start the Flask microframework:

```
./service.py
;;;

Call the service:

```
curl -i http://127.0.0.1:5000/v1/organisations?plaats=Mijnsheerenland&maxpages=2
;;;
