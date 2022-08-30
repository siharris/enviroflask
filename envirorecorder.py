from flask import Flask
from flask import current_app, flash, jsonify, make_response, redirect, request, url_for

app = Flask(__name__)

__author__ = 'Simon'


@app.route("/posts/", methods=['POST'])
def add():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.get_json()
        print(json)
        #####
        ### 1) extract sensor and then put them into a database 
        ### 2) rename service and setup 
        ### 3) Setup and run next 2 ????? 
    return jsonify({"success": "Successfully recorded reading."})







from asyncio.log import logger
from os.path import exists
from datetime import datetime

import logging
from socket import create_connection
import sys
import platform
from tempfile import gettempdir

try:
    ONWINDOWS = False
    import gpiozero as gz 
except ImportError:
    print("WARNING : gpizero only works for pi based installs, all temperature readings on windows will output -1\n")
    
import os.path
import sqlite3
import psutil
import time
import platform

DATABASE = "enviro.db"

def initLogging():
    #
    try:
        if __name__ == "__main__":

            logging.basicConfig(format='%(asctime)-15s %(levelname)s:%(message)s', level=logging.DEBUG)

            handler = logging.StreamHandler(sys.stdout)
            handler.setLevel(logging.DEBUG)
            formatter = logging.Formatter('%(asctime)-15s %(levelname)s:%(message)s')
            handler.setFormatter(formatter)
            logger = logging.getLogger(__name__)
        else:
            logger = logging.getLogger("jarvoscore")

        return logging

    except:

        e = sys.exc_info()[0]


        recordTemp()
       
def getDatabaseFilePath():
    return "%s//%s"% (os.getcwd() , DATABASE )

def doesDatabaseExist():
    ###
    ###
    ###
  
    file_exists = os.path.exists(getDatabaseFilePath())
    if file_exists:
        return True
    else:
        return False
        
        
def getConnection():
    ###
    ###
    ###
    conn = sqlite3.connect(getDatabaseFilePath()) 
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

def createTable():
    ###
    ###
    ###
    dbCursor = getConnection().cursor()
    dbCursor.execute('''CREATE TABLE IF NOT EXISTS t_pitemp
             (timestamp INTEGER NOT NULL, temperature REAL NOT NULL,PRIMARY KEY(timestamp))''')


def getTempResultCount():
    ###
    ###
    ###
    dbCursor = getConnection().cursor()
    dbCursor.execute('''SELECT COUNT(*) FROM t_pitemp AS count;''')
    row = dbCursor.fetchone()
    return row[0]


def recordTemp():
    ###
    ###
    ###
    try:
        dbConn = getConnection()
        dbCursor = dbConn.cursor()
        with dbConn:
            
            sql = ''' INSERT INTO t_pitemp(timestamp,temperature) VALUES(?,?) '''
            result = dbCursor.execute(sql,(getTimeStamp(),getPiTemp()))

    except Error as e:

        logging.error("Unable to update database %s" %e)
        


def getCpuUsage():
    return psutil.cpu_percent(1)


if __name__ == "__main__":
    logging = initLogging()
    logging.debug('Testing %s in standalone mode' %__file__)

    tsOutput = getTimeStamp()
    logging.debug('Current Timestamp %s' %str(tsOutput))

    convTimeStamp = getTimeFromTimeStamp(int(tsOutput))
    logging.debug('Time stamp converted %s' %convTimeStamp)

    temp = getPiTemp()
    logging.debug('Pi running at temperature %s ' %temp)

    percent = getCpuUsage()
    logging.debug("Pi cpu usage is %f" %percent)

    databaseExists = str(doesDatabaseExist())
    logging.debug("Database exists %s" %databaseExists)

    createTable()
    recordTemp()
    rowCount = getTempResultCount()
    logging.debug("Number of temp rows %i" %rowCount)

    databaseExists = str(doesDatabaseExist())
    logging.debug("Database exists %s" %databaseExists)
    logging.debug('Everything passed')




