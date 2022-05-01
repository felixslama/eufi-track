from geopy.geocoders import Nominatim
import requests
import re
from config import *
import json
import sqlite3
from telegram_output import broadcast


def get_country(lat, lon):
    #print(lat)
    #print(lon)
    geolocator = Nominatim(user_agent="eufi-track")
    location = geolocator.reverse("{}, {}".format(lat, lon))
    return location.raw.get('address').get('country_code')

def get_adress(lat, lon):
    geolocator = Nominatim(user_agent="eufi-track")
    location = geolocator.reverse("{}, {}".format(lat, lon))
    return location.raw.get('address').get('state') + ' ' + location.raw.get('address').get('county')

def get_new_data():
    url = "https://adsbexchange-com1.p.rapidapi.com/v2/mil/"
    headers = {
        "X-RapidAPI-Host": "adsbexchange-com1.p.rapidapi.com",
        "X-RapidAPI-Key": api_key
    }
    response = requests.request("GET", url, headers=headers)
    data = response.json()
    #save data to file
    f = open("json/data.json", "w")
    f.write(json.dumps(data))
    f.close()

    return data

def send_aircraft_by_id(id):
    #open database and get aircraft data by id
    print("send_aircraft_by_id")
    dbConnection = sqlite3.connect(db_file)
    db = dbConnection.cursor()
    db.execute("SELECT * FROM aircrafts WHERE rowid=?", (id,))
    data = db.fetchall()
    data = data[0]
    print(data)
    dbConnection.close()
    try:
        outputString = f"{data[1]} seen at {get_adress(str(data[2]), str(data[3]))} at {data[8]} UTC https://globe.adsbexchange.com/?icao={data[0]}"
    except:
        outputString = f"{data[1]} seen {data[2]},{data[3]} at {data[8]} UTC https://globe.adsbexchange.com/?icao={data[0]}"
    broadcast(outputString) # Send with Telegram
    return outputString

def import_data(cursor, data_to_import):
    for ac in data_to_import['ac']:
        #print(ac)
        alt = ""
        hexcode = ""
        spd = ""
        lat = ""
        lon = ""
        hdg = ""
        acType = ""
        try:
            acType = ac['t']
        except:
            pass
        try:
            spd = ac['gs']
        except:
            pass
        try:
            del ac['mlat']
        except:
            pass

        for k in ac.keys():
            if "heading" in k:
                hdg = ac[k]
            if "lon" in k:
                lon = ac[k]
            if "lat" in k:
                lat = ac[k]
            if "hex" in k:
                hexcode = ac[k]
            if "alt" in k:
                alt = ac[k]
        time = ac['time']
        try:
            country = get_country(lat, lon)
            #country = "empty for testing"
        except:
            pass
        #print(str(hexcode) + " " + str(acType) +" " + str(lat) + " " + str(lon) + " " + str(alt) + " " + str(spd) + " " + str(hdg) + " " + str(time) + " " + str(country))

        #write to db
        cursor.execute("INSERT INTO aircrafts VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (hexcode, acType, lat, lon, alt, spd, hdg, country, time))
