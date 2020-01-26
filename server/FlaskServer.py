from db.credentials import db_name, user, pw, db_url
from db.initialize_db import insertIntoTable
from auth_token import auth_token, usr
from flask import Flask, request, render_template, jsonify
from twilio.rest import Client
import psycopg2

# www.api.py

# rest API (front-end request things from the end-points)
# react.js app - for front-end, query flask -> database -> show to user
# showing visual statistics

# connect to "aws rds Aurora" which hosts "postgresql database" which you should query/communicate with
# https://aws.amazon.com/blogs/database/using-the-data-api-to-interact-with-an-amazon-aurora-serverless-mysql-database/
# Wael sends license plate & parking spot to server; method sends the info from a docString to the database. Post request end-point args = parkingID, licensePlate

app = Flask(__name__, template_folder='..\\show-parking-spots\\public')

@app.route('/')
def home():
    return render_template('index.html')

# http://127.0.0.1:8080/updateParkingSpot?licensePlate=H9R1K7&parkingID=1
# parkingID = 1, licensePlate = H9R1K7
@app.route('/updateParkingSpot')
def updateParkingSpot():
    licensePlate = request.args.get('licensePlate', default = 'emptyLicensePlate', type = str)
    parkingID = request.args.get('parkingID', default = 'emptyParkingID', type = str) # must cast to int
    return 'licensePlate = ' + licensePlate + ', parkingID = ' + parkingID

# query parkingSpots table, get everything and send as a json
@app.route('/getParkingSpots')
def getParkingSpots():
    return jsonify(...)

@app.route('/getHeatMaps')
def getHeatMaps():
    return "connect & query postgresql database for statistics"

# send sms when OPENING a session and when closing a session
@app.route('/smsTest')
def sms():
    client = Client('AC21e9227565ca47b0068120482bc4547d', auth_token)
    msg = 'You have just claimed your parking spot! You will now start being charged. Thank you for using Parkr! Drive safe, drive smart!'
    message = client.messages.create(from_ = '+12017293896', body = msg, to = usr)
    return 'Message ID: ' + message.sid + ', Message: ' + msg

if __name__ == '__main__':
    # Connect to the PostgreSQL database server
    conn = None
    try:
        # read connection parameters from credentials.py & connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(host = db_url, database = db_name, user = user, password = pw)
        # server running
        app.run(host='127.0.0.1', port=8080)
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')