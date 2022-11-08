from flask import Flask
from flask import current_app, flash, jsonify, make_response, redirect, request, url_for
from asyncio.log import logger
from os.path import exists
from datetime import datetime
from socket import create_connection
from tempfile import gettempdir

import logging
import sys
import platform
import os.path
import sqlite3
import sys
import time
import platform
import json

app = Flask(__name__)

__author__ = 'Simon'
DATABASE = "enviro.db"


logging.basicConfig(filename='envirorecorder.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

###  
### TODO 1) Added the nickname for the device so the service can deal with multiple devices not just one 
### TODO 2) At a retrieve interface to get data for a data range 
### TODO 3) Change post method to record 
### DONE 4) Add query interface 
### TODO 5) Add a register interface 
### TODO 6) Put in swagger interface 
### TODO 7) Put through pylint process 
### TODO 8) Add Doxygen 
### TODO 9) Put in a config file for location , database , port 
### TODO 10) Add Authentication mechanism 
###

###
###
### import urequests
###
###  auth = None
###  if config.custom_http_username:
###    auth = (config.custom_http_username, config.custom_http_password)
###
###  try:
###    # post reading data to http endpoint
###   result = urequests.post(url, auth=auth, json=reading)
###    result.close()
###    return result.status_code in [200, 201, 202]
###  except:
###    pass      
###
###  return False
###
@app.route("/posts/", methods=['POST'])
def add():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        app.logger.info('Processing sensor reading')
        jsonResult = request.get_json()
        app.logger.debug(jsonResult)
        app.logger.debug(type(jsonResult))
        for key in jsonResult:
            app.logger.debug(key)
        app.logger.debug("nickname %s" %jsonResult["nickname"])
        readings = jsonResult["readings"]
        for key,value in readings.items():
            app.logger.debug("key %s value %s" %(key,value))
            
        #####
        ### 1) extract sensor and then put them into a database 
        
        pressure = readings["pressure"]
        pm2_5 = readings["pm2_5"]
        pm10 = readings["pm10"]
        noise = readings["noise"]
        humidity = readings["humidity"]
        temperature = readings["temperature"]
        pm1 = readings["pm1"]
        timestampRaw = jsonResult["timestamp"]
        timestamp = getTimeStamp(timestampRaw)
        ###
        dbConn = getConnection()
        dbCursor = getConnection().cursor()
        ### 
        ### dbCursor.execute('''CREATE TABLE IF NOT EXISTS t_enviro
        ###     (timestamp INTEGER NOT NULL, temperature REAL NOT NULL, humidity REAL NOT NULL, pressure REAL NOT NULL, lux REAL NOT NULL, col_temp INTEGER NOT NULL, PRIMARY KEY(timestamp))''')
        ###
        ###
        ###    dbCursor.execute('''CREATE TABLE IF NOT EXISTS t_enviro (
        ###                timestamp INTEGER NOT NULL,
        ###                pressure REAL NOT NULL,
        ###                pm2_5 INTEGER NOT NULL,
        ###                pm10 INTEGER NOT NULL,
        ###                noise REAL NOT NULL,
        ###                humidity REAL NOT NULL,
        ###                temperature REAL NOT NULL,
        ###                pm1 INTEGER NOT NULL,
        ###                PRIMARY KEY(timestamp))''')
        ###
        ###


        try:        
            with dbConn: 
                sql = ''' INSERT INTO t_enviro(timestamp,pressure,pm2_5,pm10,noise,humidity,temperature,pm1) VALUES(?,?,?,?,?,?,?,?) '''
                result = dbCursor.execute(sql,(timestamp,pressure,pm2_5,pm10,noise,humidity,temperature,pm1))
                app.logger.debug("Insert to DB executed result %s" %result)

        except:
            app.logger.error("Unable to update database %s" %sys.exc_info()[0])
            return jsonify({"failure": "Unable to record reading check server log"})

    return jsonify({"success": "Successfully recorded reading."})

@app.route('/query', methods=['GET'])
def query():
    args = request.args
    if len(args) == 0:
        return jsonify(getReadingsCount())
    else:
        dateFrom = request.args.get('range')
        return jsonify(getReadingStartingFrom(dateFrom))

   
       
def getDatabaseFilePath():
    return "%s//%s"% (os.getcwd() , DATABASE )
        

def getReadingsCount():

    
    queryString = ('SELECT count(*) FROM t_enviro')    
    logging.debug('Reading EnviroDB %s ' %__file__)
    logging.debug("sql script %s",queryString)
    dbConn = getConnection()
    dbCursor = getConnection().cursor()
    dbCursor.execute(queryString)
    row = dbCursor.fetchone()
    count = row[0]
    result = {"count":str(count)}
    return result

def getReadingStartingFrom(dateFrom):
    
    logging.debug("Extracting DateFrom %s",dateFrom)
    queryString = ('SELECT * FROM t_enviro WHERE timestamp > %s;' %int(getTimeStampDay(dateFrom)))     
    logging.debug('Reading EnviroDB %s ' %__file__)
    logging.debug("sql script %s",queryString)
    dbConn = getConnection()
    dbCursor = getConnection().cursor()
    dbCursor.execute(queryString)
        
    cnt=0
    result = {}
    for row in dbCursor.execute(queryString):
        result[cnt] = {"TimeStamp": getTimeFromTimeStamp(row[0]) , "Pressure": str(row[1]),"pm2_5" : str(row[2]) ,"pm10" : str(row[3]) ,
        "noise" : str(row[4]), "humidity" : str(row[5]),"temperature" :str(row[6]),"pm1" : str(row[7])}
        cnt=cnt+1
    return result


def getConnection():
    ###
    ###
    ###
    conn = sqlite3.connect(getDatabaseFilePath(), isolation_level=None) 
    return conn

def getTimeStamp(timeStampString):
    ###
    ###
    ###
    timeStamp = datetime.strptime(timeStampString, "%Y-%m-%d %H:%M:%S").timestamp()
    app.logger.debug('Current timestamp %s' %timeStamp)
    return timeStamp

def getTimeFromTimeStamp(timeStamp):
    ###
    ###
    ###
    timeStamp2 = datetime.fromtimestamp(timeStamp)
    timeStamp2.strftime('%Y-%m-%d %H:%M:%S')
    app.logger.debug('Returning normal time from timestamp %s' %timeStamp2)
    return timeStamp2

def getTimeStampDay(timeStampString):
    ###
    ###
    ###
    timeStampDay = datetime.strptime(timeStampString, "%Y-%m-%d").timestamp()
    app.logger.debug('Current timestamp %s' %timeStampDay)
    return timeStampDay

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000)