
from asyncio.log import logger
from os.path import exists
from datetime import datetime
from tempfile import gettempdir
from socket import create_connection

import sys
import platform
import logging
import os.path
import sqlite3
import sys
import time
import platform

__author__ = 'Simon'


DATABASE = "enviro.db"


def initLogging():
    #
    try:
        logging.basicConfig(format='%(asctime)-15s %(levelname)s:%(message)s', level=logging.DEBUG)

        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)-15s %(levelname)s:%(message)s')
        handler.setFormatter(formatter)
        logger = logging.getLogger(__name__)
        return logging

    except:

        e = sys.exc_info()[0]

def getDatabaseFilePath():
    return "%s//%s"% (os.getcwd() , DATABASE )
        
        
def getConnection():
    ###
    ###
    ###
    conn = sqlite3.connect(getDatabaseFilePath(), isolation_level=None) 
    return conn

###
###2022-09-05 17:48:09,749 DEBUG envirorecorder Thread-5 : <class 'dict'>
###2022-09-05 17:48:09,750 DEBUG envirorecorder Thread-5 : readings
###2022-09-05 17:48:09,750 DEBUG envirorecorder Thread-5 : nickname
###2022-09-05 17:48:09,751 DEBUG envirorecorder Thread-5 : timestamp
###2022-09-05 17:48:09,751 DEBUG envirorecorder Thread-5 : nickname enviropi-01
###2022-09-05 17:48:09,752 DEBUG envirorecorder Thread-5 : key pressure value 1010.37
###2022-09-05 17:48:09,752 DEBUG envirorecorder Thread-5 : key pm2_5 value 24
###2022-09-05 17:48:09,753 DEBUG envirorecorder Thread-5 : key pm10 value 34
###2022-09-05 17:48:09,754 DEBUG envirorecorder Thread-5 : key noise value 1.5
###2022-09-05 17:48:09,754 DEBUG envirorecorder Thread-5 : key humidity value 53.01
###2022-09-05 17:48:09,755 DEBUG envirorecorder Thread-5 : key temperature value 27.62
###2022-09-05 17:48:09,755 DEBUG envirorecorder Thread-5 : key pm1 value 8
###2022-09-05 17:48:09,756 ERROR envirorecorder Thread-5 : Exception on /posts/ [POST]

if __name__ == "__main__":
    logging = initLogging()
    logging.debug('Creating EnviroDB %s ' %__file__)
    dbConn = getConnection()
    dbCursor = getConnection().cursor()
    dbCursor.execute('''CREATE TABLE IF NOT EXISTS t_enviro (
                        timestamp INTEGER NOT NULL,
                        pressure REAL NOT NULL,
                        pm2_5 INTEGER NOT NULL,
                        pm10 INTEGER NOT NULL,
                        noise REAL NOT NULL,
                        humidity REAL NOT NULL,
                        temperature REAL NOT NULL,
                        pm1 INTEGER NOT NULL,
                        PRIMARY KEY(timestamp))''')
    logging.debug('Created DB complete')
