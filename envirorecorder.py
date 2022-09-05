from flask import Flask
from flask import current_app, flash, jsonify, make_response, redirect, request, url_for
from asyncio.log import logger
from os.path import exists
from datetime import datetime

import logging
from socket import create_connection
import sys
import platform
from tempfile import gettempdir
import os.path
import sqlite3
import sys


import time
import platform

app = Flask(__name__)

__author__ = 'Simon'


DATABASE = "enviro.db"


logging.basicConfig(filename='envirorecorder.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')



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
        temperature = readings["temperature"]
        humidity = readings["humidity"]
        pressure = readings["pressure"]
        lux = readings["lux"]
        colour_temp = readings["colour_temperature"]
        timestamp = getTimeStamp()
        ###
        dbConn = getConnection()
        dbCursor = getConnection().cursor()
        ### 
        ### dbCursor.execute('''CREATE TABLE IF NOT EXISTS t_enviro
        ###     (timestamp INTEGER NOT NULL, temperature REAL NOT NULL, humidity REAL NOT NULL, pressure REAL NOT NULL, lux REAL NOT NULL, col_temp INTEGER NOT NULL, PRIMARY KEY(timestamp))''')
        try:        
            with dbConn: 
                sql = ''' INSERT INTO t_enviro(timestamp,temperature,humidity,pressure,lux,col_temp) VALUES(?,?,?,?,?,?) '''
                result = dbCursor.execute(sql,(timestamp,temperature,humidity,pressure,lux,colour_temp))
                app.logger.debug("Insert to DB executed result %s" %result)

        except:
            app.logger.error("Unable to update database %s" %sys.exc_info()[0])
            return jsonify({"failure": "Unable to record reading check server log"})

    return jsonify({"success": "Successfully recorded reading."})


       
def getDatabaseFilePath():
    return "%s//%s"% (os.getcwd() , DATABASE )
        
        
def getConnection():
    ###
    ###
    ###
    conn = sqlite3.connect(getDatabaseFilePath(), isolation_level=None) 
    return conn

def getTimeStamp():
    ###
    ###
    ###
    curr_dt = datetime.now()
    timeStamp = str(int(round(curr_dt.timestamp())))
    logging.debug('Current timestamp %s' %timeStamp)
    return timeStamp

def getTimeFromTimeStamp(timeStamp):
    ###
    ###
    ###
    timeStamp2 = datetime.fromtimestamp(timeStamp)
    timeStamp2.strftime('%Y-%m-%d %H:%M:%S')
    logging.debug('Returning normal time from timestamp %s' %timeStamp2)
    return timeStamp2