import json
import sys
import re
import os
import csv
from cache import *
import pandas as pd
from database import *


BASE_URL = 'http://www.planecrashinfo.com'


headers = {
    'User-Agent': 'UMSI 507 Course Project - Python Scraping',
    'From': 'eamini@umich.edu',
    'Course-Info': 'https://si.umich.edu/programs/courses/507'
}

CACHE_DICT = load_cache()
crash_list = []

class Crash:
    '''a crash

    Instance Attributes
    -------------------
    date: string
        the date of crash (e.g. 'September 17, 1908')

    time: string
        the time of crash(e.g. '1718')

    location: string
        the location of the crash (e.g. 'Fort Myer, Virginia')

    flight_num: int
        flight number (e.g. '6491')

    route: string
        route of flight (e.g. 'Hong Kong - Bishkek - Istanbul')

    ac_type: string
        aircraft type (e.g. 'Boeing 747-412F')

    operator: string
        operator (e.g. "My Cargo Airlines (ACT Airlines)")

    abroad:int

    fatalities: int

    ground: int

    summary: string
        summary of crashes
    '''

    def __init__(self, date="No date", time="No time",
                 location="No location", country="No country",
                 departure="No departure", destination="No destination",
                 acType="No ac_type", operator="No Operator",
                 occupants="No occupants", fatalities="No Fatalities",
                 summary="No Summary"):
        self.date = date
        self.time = time
        self.location = location
        self.country = country
        self.departure = departure
        self.destination = destination
        self.acType = acType
        self.operator = operator
        self.occupants = occupants
        self.fatalities = fatalities
        self.summary = summary

    def info(self):
        return f'{self.date} ({self.time}): {self.location} {self.country}'




def build_crash_year_url_dict():
    ''' Make a dictionary that maps crashes' years to their url from "https://www.planecrashinfo.com"

    Parameters
    ----------
    None

    Returns
    -------
    dict
        key is a year and value is the url
        e.g. {'1920':'http://www.planecrashinfo.com/1920/1920.htm', ...}
    '''
    DATABASE_PAGE_PATH = '/database.htm'
    year_url_dict = {}
    response = make_url_request_using_cache(BASE_URL+DATABASE_PAGE_PATH, CACHE_DICT)
    if response:
        soup = BeautifulSoup(response, 'html.parser')
        table = soup.find_all('table')[1]

        table_rows = table.find_all('tr')
        for tr in table_rows:
            td = tr.find_all('td')
            for i in td:
                if i.find('a') is not None:
                    year_partial_url = i.find('a')['href']
                    if year_partial_url.startswith('/'):
                        year_url = BASE_URL+year_partial_url
                    else:
                        year_url = BASE_URL+'/'+year_partial_url
                    year = i.text.strip()
                    year_url_dict[year] = year_url

    return year_url_dict

def get_crash_instance(crash_url):
    '''Make an instances from a crash url.

    Parameters
    ----------
    crash_url: string
        The URL for a crash

    Returns
    -------
    instance
        a crash instance
    '''
    date = None
    time = None
    location = None
    country = None
    operator = None
    departure = None
    destination = None
    acType = None
    occupants = None
    fatalities = None
    summary = None

    response = make_url_request_using_cache(crash_url, CACHE_DICT)
    if response:
        soup = BeautifulSoup(response, 'html.parser')
        table = soup.find('table')
        table_rows = soup.find_all('tr')
        for tr in table_rows[1:]:
            td = tr.find_all('td')
            if td[0].text.strip() == "Date:" and td[1].text.strip() != '?':
                date = td[1].text.strip()
            if td[0].text.strip() == "Location:" and td[1].text.strip() != '?':
                if ',' in td[1].text.strip():
                    loc = td[1].text.strip()
                    location = loc.split(',')[0].strip()
                    country =  loc.split(',')[1].strip()
                else:
                    location = td[1].text.strip()
            if td[0].text.strip() == "Route:" and td[1].text.strip() != '?':
                if '-' in td[1].text.strip():
                    departure = td[1].text.strip().split('-')[0].strip()
                    destination = td[1].text.strip().split('-')[1].strip()
                else:
                    departure = td[1].text.strip()
            if td[0].text.strip().startswith("AC") and td[1].text.strip() != '?':
                acType = td[1].text.strip()
            if td[0].text.strip() == "Operator:" and td[1].text.strip() != '?':
                operator = td[1].text.strip()
            if td[0].text.strip() == "Aboard:" and td[1].text.strip().startswith('?') is False:
                occupants = re.sub(r'\(.*','', td[1].text.strip())
                #occupants = int(occupants_text)
            if td[0].text.strip() == "Fatalities:" and td[1].text.strip().startswith('?') is False:
                fatalities = re.sub(r'\(.*','', td[1].text.strip())
                #fatalities = int(fatalities_text)
            if td[0].text.strip() == "Summary:" and td[1].text.strip() != '?':
                summary = td[1].text.strip()

        return Crash(date, time, location, country, departure, destination, acType, operator, occupants, fatalities, summary)





def get_year_instance(year_url):
    '''Make an instances from a year URL.

    Parameters
    ----------
    year_url: string
        The URL for a year in planecrashinfo.com

    Returns
    -------
    instance
        a year instance
    '''
    crash_instance_list = []
    print(year_url)

    response = make_url_request_using_cache(year_url, CACHE_DICT)
    if response:
        soup = BeautifulSoup(response, 'html.parser')
        table = soup.find('table')
        table_rows = soup.find_all('tr')
        for tr in table_rows:
            td = tr.find_all('td')
            for i in td:
                if i.find('a') is not None:
                    year_partial_url = i.find('a')['href']
                    head, tail = os.path.split(year_url)
                    crash_url = head+'/'+year_partial_url
                    crash_instance = get_crash_instance(crash_url)
                    crash_instance_list.append(crash_instance)

    return crash_instance_list


if __name__ == "__main__":
    crash_instance_list = []
    url_dict = build_crash_year_url_dict()
    for k, v in url_dict.items():
        c=get_year_instance(v)
        crash_instance_list.append(c)



    with open('data/crash_original_format_from_web.csv', mode='w') as crash_file:

        crash_writer = csv.writer(crash_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for list in crash_instance_list:
            for item in list:
                crash_writer.writerow([item.date, item.location, item.country, item.departure,
                                       item.destination, item.acType, item.operator, item.occupants, item.fatalities, item.summary])
