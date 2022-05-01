from itertools import count
import sched, time
from config import *
from utility import *
import sqlite3
import json
import time
import pandas as pd
from datetime import datetime
new_data = False

if new_data == True:
    get_new_data()

#check if table exists before writeing to it
#write to database
s = sched.scheduler(time.time, time.sleep)
def main_loop(sc):
    dbConnection = sqlite3.connect(db_file)
    db = dbConnection.cursor()

    sql_file = open("sql/table.sqlite")
    sql_commands = sql_file.read()
    db.executescript(sql_commands)

    print("begin mainloop")
    current_data = get_new_data()
    #append time to every aircraft in data
    data_time_received = datetime.utcfromtimestamp(current_data['ctime']/1000).strftime('%Y-%m-%d %H:%M:%S')
    for ac in current_data['ac']:
        ac["time"] = (data_time_received)
    import_data(db, current_data)
    #print(count(current_data['ac']))
    db.execute("SELECT rowid, * FROM aircrafts WHERE time=? AND country=? AND NOT lat='' AND NOT lon='' AND NOT alt='' AND NOT spd=''", (data_time_received, country_to_alert))
    ac_in_country = db.fetchall()
    dbConnection.commit()
    dbConnection.close()
    for ac in ac_in_country:
        print(ac[0])
        send_aircraft_by_id(ac[0])
    

    sc.enter(delay_between_requests, 1, main_loop, (sc,))

#run main loop every 60 seconds
s.enter(1, 1, main_loop, (s,))
s.run()

print('status')
#print(send_aircraft_by_id(69))


dbConnection.commit()
dbConnection.close()