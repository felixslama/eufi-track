from curses.ascii import alt
from config import *
from utility import *
import requests
import sqlite3
import json
import time
import pandas as pd
import os
import re
from datetime import datetime
new_data = False

if new_data == True:
    get_new_data()

#establish connection to db
dbConnection = sqlite3.connect(db_file)
db = dbConnection.cursor()

data = json.load(open('json/data.json'))

#append time to every aircraft in data
data_time_received = datetime.utcfromtimestamp(data['ctime']/1000).strftime('%Y-%m-%d %H:%M:%S')
for ac in data['ac']:
    ac["time"] = (data_time_received)
    #print(ac)
    #print("\n")

#check if table exists before writeing to it
sql_file = open("sql/table.sqlite")
sql_commands = sql_file.read()
db.executescript(sql_commands)
#write to database
#import_data(db, data)
print(send_aircraft_by_id(69))

#print all data in table
#db.execute("SELECT * FROM aircrafts")
#print(db.fetchall())
dbConnection.commit()
dbConnection.close()