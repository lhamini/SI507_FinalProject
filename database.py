import csv
import sqlite3
from plane_crash import *

DB_NAME = "PlaneCrashes.sqlite"

def create_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    drop_week_sql = 'DROP TABLE IF EXISTS "Week"'
    drop_phase_sql = 'DROP TABLE IF EXISTS "Phase"'
    drop_category_sql = 'DROP TABLE IF EXISTS "Category"'
    drop_aircraft_sql = 'DROP TABLE IF EXISTS "Aircrafts"'
    drop_countries_sql = 'DROP TABLE IF EXISTS "Countries"'
    drop_airports_sql = 'DROP TABLE IF EXISTS "Airports"'
    drop_crashes_sql = 'DROP TABLE IF EXISTS "Crashes"'

    create_aircraft_sql = '''
        CREATE TABLE IF NOT EXISTS "Aircrafts" (
            "Id" INTEGER PRIMARY KEY AUTOINCREMENT,
            "aircraft_model" TEXT NOT NULL,
            "Eegines" TEXT NOT NULL,
            "first flight" Text NOT NULL
        )
    '''

    create_countries_sql = '''
        CREATE TABLE IF NOT EXISTS "Countries" (
            "Id" INTEGER PRIMARY KEY AUTOINCREMENT,
            "name" TEXT NOT NULL,
            "alpha2Code" TEXT NOT NULL,
            "alpha3Code" TEXT NOT NULL,
            "region" Text NOT NULL,
            "latlng" Text NOT NULL,
            "flag" Text NOT NULL
        )
    '''

    create_crashes_sql = '''
        CREATE TABLE IF NOT EXISTS "Crashes" (
            "Id" INTEGER PRIMARY KEY AUTOINCREMENT,
            "date" INTEGER,
            "location" TEXT,
            "countryId" INTEGER,
            "departure" TEXT,
            "destination" TEXT,
            "acTypeId" INTEGER,
            "operator" TEXT,
            "occupants" INTEGER,
            "fatalities" INTEGER,
            "summary" TEXT
        )
    '''

    cur.execute(drop_aircraft_sql)
    cur.execute(drop_countries_sql)
    cur.execute(drop_crashes_sql)

    cur.execute(create_aircraft_sql)
    cur.execute(create_countries_sql)
    cur.execute(create_crashes_sql)

    conn.commit()
    conn.close()


def load_aircrafts():
    file_contents = open('data/aircrafts.csv', 'r')
    csv_reader = csv.reader(file_contents)
    next(csv_reader)

    insert_aircrafts_sql = '''
        INSERT INTO Aircrafts
        VALUES (NULL, ?, ?, ?)
    '''

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    for r in csv_reader:
        cur.execute(insert_aircrafts_sql, [r[0], r[1], r[2]])

    conn.commit()
    conn.close()

def load_countries():
    file_contents = open('data/countries.csv', 'r')
    csv_reader = csv.reader(file_contents)
    next(csv_reader)

    insert_countries_sql = '''
        INSERT INTO Countries
        VALUES (NULL, ?, ?, ?, ?, ?, ?)
    '''

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    for r in csv_reader:
        cur.execute(insert_countries_sql, [r[1], r[2], r[3], r[4], r[5], r[7]])

    conn.commit()
    conn.close()

def load_airports():
    file_contents = open('data/airports.csv', 'r')
    csv_reader = csv.reader(file_contents)
    next(csv_reader)

    insert_airports_sql = '''
        INSERT INTO Airports
        VALUES (NULL, ?, ?, ?)
    '''

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    for r in csv_reader:
        cur.execute(insert_airports_sql, [r[0], r[1], r[2]])

    conn.commit()
    conn.close()

def load_crashes():
    file_contents = open('data/crash.csv', 'r')
    csv_reader = csv.reader(file_contents)
    next(csv_reader)

    fc = open('data/aircrafts.csv')
    cr = csv.reader(fc)
    next(cr)

    select_country_id_sql = '''
        SELECT Id From Countries
        WHERE name = ?
    '''

    select_aircraft_id_sql = '''
        SELECT Id FROM Aircrafts
        WHERE aircraft_model = ?
    '''

    insert_crash_sql = '''
        INSERT INTO Crashes
        VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    '''


    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()


    for r in csv_reader:
        cur.execute(select_country_id_sql, [r[3]])
        res = cur.fetchone()
        crash_country_id = None
        if res is not None:
            crash_country_id = res[0]

        cur.execute(select_aircraft_id_sql, [r[6]])
        res = cur.fetchone()
        crash_aircraft_id = None
        if res is not None:
            crash_aircraft_id = res[0]


        cur.execute(insert_crash_sql, [
        r[1],
        r[2],
        crash_country_id,
        r[4],
        r[5],
        crash_aircraft_id,
        r[7],
        r[8],
        r[9],
        r[10]
        ])


    conn.commit()
    conn.close()



create_db()
load_aircrafts()
load_countries()
load_crashes()
