#!/usr/bin/python3

import csv
import logging
import logger_init
from search import Search
from models import Session, Company
from time import sleep

logger = logging.getLogger("webscraper_app.company_scraper")

def process_company(kvk_number):
    filter = {
        "handelsnaam": "",
        "kvknummer": kvk_number,
        "straat": "",
        "huisnummer": "",
        "postcode": "",
        "plaats": "",
        "hoofdvestiging": "true",
        "nevenvestiging": "true",
        "rechtspersoon": "true",
        "vervallen": "0",
        "uitgeschreven": "0"
    }
    
    search = Search(filter, 1, 1)
    results = search.run()
    if results and results["organisaties"]:
        return results["organisaties"][0]
    return None

def main():
    session = Session()
    
    with open('input_companies.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            kvk = row['kvk_number']
            logger.info(f"Processing KVK number: {kvk}")
            
            # Check if company already exists
            if session.query(Company).filter_by(kvk_number=kvk).first():
                logger.info(f"Company {kvk} already exists, skipping")
                continue
                
            try:
                company_data = process_company(kvk)
                if company_data:
                    company = Company(
                        kvk_number=company_data['kvk_nummer'],
                        company_name=company_data['handelsnaam'],
                        street=company_data['adres'].get('straat', ''),
                        house_number=company_data['adres'].get('huisnummer', ''),
                        postcode=company_data['adres'].get('postcode', ''),
                        city=company_data['adres'].get('plaats', ''),
                        is_main_establishment='hoofdvestiging' in company_data,
                        establishment_number=company_data.get('vestigingsnr', ''),
                        is_branch='nevenvestiging' in company_data
                    )
                    session.add(company)
                    session.commit()
                    logger.info(f"Saved company {kvk}")
                
                # Be nice to the KVK website
                sleep(2)
                
            except Exception as e:
                logger.error(f"Error processing {kvk}: {str(e)}")
                session.rollback()
                
    session.close()

if __name__ == "__main__":
    main()
