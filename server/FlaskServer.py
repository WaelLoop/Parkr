from db.credentials import db_name, user, pw, db_url
from db.initialize_db import insertIntoTable, resetDB, seed
from db.queries import updateParkingSpot, getTableValueByName, getAllParkingSpots
from auth_token import auth_token, usr
from db.sql.tables import tables
from flask import Flask, request
from twilio.rest import Client
import psycopg2
import sys
import json
from datetime import datetime, timedelta

# www.api.py

# rest API (front-end request things from the end-points)
# react.js app - for front-end, query flask -> database -> show to user
# showing visual statistics

# connect to "aws rds Aurora" which hosts "postgresql database" which you should query/communicate with
# https://aws.amazon.com/blogs/database/using-the-data-api-to-interact-with-an-amazon-aurora-serverless-mysql-database/
# Wael sends license plate & parking spot to server; method sends the info from a docString to the database. Post request end-point args = parkingID, licensePlate

app = Flask(__name__)

conn = None

def sendSMS(msg,usr):
    client = Client('AC21e9227565ca47b0068120482bc4547d', auth_token)
    message = client.messages.create(from_ = '+12017293896', body = msg, to = usr)
    return 'Message ID: ' + message.sid + ', Message: ' + msg

def splitDate(dateTime):
    [date, time] = dateTime.split(" ")
    date = date.split('-')
    time = time.split('.')[0].split(':')

    for i in range(len(date)):
        date[i] = int(date[i])
        if i == 0:
            time[i] = int(time[i])+5
        else:
            time[i] = int(time[i])
    
    return datetime(date[0],date[1],date[2],time[0],time[1],time[2])

def duration(startTime, endTime):
    # d1 = splitDate(startTime)
    # d2 = splitDate(endTime)
    duration = (endTime-startTime).seconds
    return (duration//60, duration%60)

@app.route('/')
def home():
    return 'Parkr'

# http://127.0.0.1:8080/updateParkingSpot?licensePlate=H9R1K7&parkingID=1
# parkingID = 1, licensePlate = H9R1K7
@app.route('/updateParkingSpot')
def updateSpot():
    licensePlate = request.args.get('licensePlate', default = 'emptyLicensePlate', type = str)
    parkingID = request.args.get('parkingID', default = 'emptyParkingID', type = str) # must cast to int
    
    if licensePlate == "":
        licensePlate = None
    else:
        licensePlate = licensePlate.upper()

    res = updateParkingSpot(conn,licensePlate, parkingID)
    print('result', res)
    if res is not None:
        userId, sessionId = res;
        phone = getTableValueByName(conn, 'person', 'phone_num', ('id',userId))

        startTime = getTableValueByName(conn, 'parking_sessions','start_time',('id',sessionId))
        endTime = getTableValueByName(conn, 'parking_sessions', 'end_time', ('id',sessionId))

        dur = duration(startTime, endTime)

        if phone is not None:
            sendSMS(f"Don't forget to pay for parking {dur[0]} minutes and {dur[1]} seconds!",phone)

    return 'licensePlate = ' +  '' if licensePlate is None else licensePlate + ', parkingID = ' + parkingID

# query parkingSpots table, get everything and send as a json
@app.route('/getParkingSpots')
def getParkingSpots():
    spots = getAllParkingSpots(conn)
    data = {}
    data['result'] = spots
    json_data = json.dumps(data)
    return json_data

@app.route('/getHeatMaps')
def getHeatMaps():
    return "connect & query postgresql database for statistics"

if __name__ == '__main__':
    # Connect to the PostgreSQL database server
    conn = None
    try:
        # read connection parameters from credentials.py & connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(host = db_url, database = db_name, user = user, password = pw)

        #reset the db at the start of the app
        resetDB(conn,tables)
        #seed the db
        seed(conn, tables)

        # server running
        app.run(host='127.0.0.1', port=5000)
        
    except (Exception, psycopg2.DatabaseError) as error:
        e = sys.exc_info()[0]
        print(f"{e}")
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')