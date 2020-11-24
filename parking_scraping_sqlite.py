from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl
import re
import os
from datetime import datetime
import sqlite3
import schedule
import time

# open database
conn = sqlite3.connect('parkingData_2.0.sqlite')
cur = conn.cursor()

# Setup a table
cur.executescript('''

DROP TABLE IF EXISTS ParkingData;

CREATE TABLE ParkingData (
    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    kustaankatu_payment   INTEGER,
    kustaankatu_contract   INTEGER,
    flemingingkatu_payment  INTEGER,
    flemingingkatu_contract INTEGER,
    tmstp  TEXT
);

''')

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


def scrape():

    url = 'http://www.vallilaparking.com/'
    html = urlopen(url, context=ctx).read()
    soup = BeautifulSoup(html, "html.parser")

    # Retrieve all of the div tags
    divs = soup('div')

    parking_places_number = []

    print("Scraping ...")
    # search for the relevant div's
    for div in divs:

        if re.search('^[0-9]', str(div.contents[0])):
            parking_places_number.append(int(div.contents[0]))
            print(div.contents[0])

    kustaankatu_payment = parking_places_number[0]
    kustaankatu_contract = parking_places_number[1]
    flemingingkatu_payment = parking_places_number[2]
    flemingingkatu_contract = parking_places_number[3]
    print("parking_places_number", parking_places_number)
    parking_places_number = []

    # insert srapped data in to the database
    cur.execute('''INSERT OR IGNORE INTO ParkingData (kustaankatu_payment, kustaankatu_contract, flemingingkatu_payment, flemingingkatu_contract, tmstp)
                VALUES ( ?, ?, ?, ?, ? )''', (kustaankatu_payment, kustaankatu_contract, flemingingkatu_payment, flemingingkatu_contract, datetime.now()))
    conn.commit()

    print("parking_places_number", parking_places_number)


# set the scraping interval and number of repetitions
count = 0
while count < 500:
    scrape()
    time.sleep(3)
    count = count + 1
    print("count + 1")
