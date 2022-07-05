"""
server.py allows the creation of servers, that will pull the time from the atomic clock API, and will broadcast it to clients
across a local socket connection
"""
from sys import stderr
import requests
from datetime import datetime

import logging

# instanciate logger
logger = logging.getLogger("time-server")

# get the time from the https://worldtimeapi.org/

apiEndpoint: str = "http://worldtimeapi.org/api/timezone/Europe/Paris"
response = requests.get(apiEndpoint)

dateTime = ""
date = ""
time = ""

try:
    dateTime = response.json()["datetime"]
except:
    logger.error("Enable to fetch time from worldtimeapi.org, retrying in 5min")

if dateTime:
    parsedDateTime = datetime.fromisoformat(dateTime)
    date = parsedDateTime.date()
    time = parsedDateTime.time()
    logger.info(f"New datetime successfully fetched {date} - {time}")
