"""
server.py allows the creation of servers, that will pull the time from the atomic clock API, and will broadcast it to clients
across a local socket connection.
It works across two threads:
- The first one will periodically fetch the worldtimeapi.org API to get and parse a JSON containing the date and time
- The second one will listen to request from clients and serve them the date it get in memory
"""
from sys import stderr
import requests
from datetime import datetime
import logging
import asyncio

# instanciate logger
logger = logging.getLogger("time-server")
apiEndpoint: str = "http://worldtimeapi.org/api/timezone/Europe/Paris"

# get the time from the https://worldtimeapi.org/


def fetchDateTimeFromApi():
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
        print(f"New datetime successfully fetched {date} - {time}")

async def infiniteLoop(interval:int) -> None:
    while 1:
        fetchDateTimeFromApi()
        await asyncio.sleep(interval)

asyncio.run(infiniteLoop(2))