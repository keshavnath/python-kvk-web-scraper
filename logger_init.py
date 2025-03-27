#!/usr/bin/python3

import logging

logger = logging.getLogger("webscraper_app")

# Create file handler
fh = logging.FileHandler("webscraper_app.log")
logger.setLevel(logging.DEBUG)

# Create console handler
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# Create formatter and add it to handlers
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# Add handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)

logger.debug("Logging initialized")
