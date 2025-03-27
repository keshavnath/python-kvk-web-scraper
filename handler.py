#!/usr/bin/python3

from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.parse import urlencode
import json
import re
import logging

class Handler:
    'Web scraper for the KvK website search functionality'
    search_url = ""
    logger = None

    def __init__(self, search_url):
        self.search_url = search_url
        self.logger = logging.getLogger("webscraper_app.handler")

    def has_hoofdvestiging_tag(self, search_result):
        result = search_result.find("a", class_="hoofdvestigingTag")
        if result is None:
            return False
        else:
            return True

    def retrieve_aantal_resultaten(self, searchpage):
        aantal = 0
        feedback = searchpage.find("div", class_="feedback")
        if feedback is not None:
            aantal = feedback.text[0 : feedback.text.find(" ")]
        return int(aantal)

    def calc_aantal_paginas(self, aantal_resultaten):
        rest = aantal_resultaten % 10
        if rest > 0:
            add_page = 1
        else:
            add_page = 0
        return (aantal_resultaten / 10) + add_page

    def retrieve_kvk_meta(self, organisatie, kvk_meta):
        adres = {}
        adres_cnt = 0
        adres_fields = ("straat", "huisnummer", "postcode", "plaats")
        organisatie["adres"] = adres
        
        for li in kvk_meta.find_all("li"):
            if li.string is not None:
                value = li.string.strip()
                if len(value) > 0:
                    if value.startswith("KVK"):
                        organisatie["kvk_nummer"] = value[4:].strip()
                    elif value.startswith("Vestigingsnr."):
                        organisatie["vestigingsnr"] = value[14:].strip()
                    elif value.startswith("Nevenvestiging"):
                        organisatie["nevenvestiging"] = True
                    elif value.startswith("Hoofdvestiging"):
                        organisatie["hoofdvestiging"] = True
                    else:
                        if adres_cnt < len(adres_fields):
                            adres[adres_fields[adres_cnt]] = value
                            adres_cnt += 1

    def retrieve_organisaties(self, organisaties, searchpage):
        for li in searchpage.find_all("li", class_="type1"):
            organisatie = {}
            handelsnaam = li.find("h3", class_="handelsnaamHeader")
            organisatie["handelsnaam"] = handelsnaam.a.string
            self.retrieve_kvk_meta(organisatie, li.find("ul", class_="kvk-meta"))
            if (self.has_hoofdvestiging_tag(li)):
                organisatie["hoofdvestiging"] = "Hoofdvestiging, "
            organisaties.append(organisatie)
        return organisaties 

    def load_searchpage(self):
        request = urlopen(self.search_url)
        response = request.read()
        json_encoded = response[response.find("(") + 1 : response.find(");")]
        # Fix bug that the json decoder throws an error if the special tab character (\t) if found in the text
        json_encoded = json_encoded.replace("\t", " ")
        # Fix bug that if a backslash is used in text the json decoder throws an error
        json_encoded = re.sub(r'(\\)(?![\"\'abfnrtv])', r'\\\1', json_encoded)
        try:
            json_decoded = json.loads(json_encoded)
        except ValueError as e:
            message = "Error decoding json, check html_respons.html and encoded.json [" + str(e) + "]"
            self.logger.error(message + "\n --- response --- \n" + response + "\n --- json_encoded:\n" + json_encoded)
            raise Exception(message)
        else:
            try:
                soup = BeautifulSoup(json_decoded["html"], "lxml")
            except KeyError as e:
                message = "No results [" + str(e) + "]"
                self.logger.error(message + "\n --- json_encoded --- \n" + response + "\n --- json_encoded:\n" + json_encoded)
                raise NoResultsError(message)
            else:
                searchpage = soup.find("div", class_="searchpage")
                if searchpage is None:
                    raise "Search page not found"
                return searchpage

    def init(self):
        searchpage = self.load_searchpage()
        search_results = {}
        search_results["results"] = self.retrieve_aantal_resultaten(searchpage)
        search_results["pages"] = self.calc_aantal_paginas(search_results["results"])
        return search_results

class NoResultsError(Exception):
    def __init__(self, arg):
        # Set some exception infomation
        self.msg = arg
