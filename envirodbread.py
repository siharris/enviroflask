
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

__author__ = 'simond4'


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


def getTimeFromTimeStamp(timeStamp):
    ###
    ###
    ###
    timeStamp2 = datetime.fromtimestamp(timeStamp)
    timeStamp2.strftime('%Y-%m-%d %H:%M:%S')
    logger.debug('Returning normal time from timestamp %s' %timeStamp2)
    return timeStamp2

def getTimeStamp(timeStampString):
    ###
    ###
    ###
    timeStamp = datetime.strptime(timeStampString, "%Y-%m-%d %H:%M:%S").timestamp()
    logger.debug('Current timestamp %s' %timeStamp)
    return timeStamp


def getTimeStampDay(timeStampString):
    ###
    ###
    ###
    timeStampDay = datetime.strptime(timeStampString, "%Y-%m-%d").timestamp()
    logger.debug('Current timestamp %s' %timeStampDay)
    return timeStampDay

if __name__ == "__main__":
    logging = initLogging()

    logging.debug(f"Arguments count: {len(sys.argv)}")
    for i, arg in enumerate(sys.argv):
        logging.debug(f"Argument {i:>6}: {arg}")

    if(len(sys.argv) > 1):
        dateFrom = sys.argv[1]
        logging.debug("Extracting DateFrom %s",dateFrom)
        queryString = ('SELECT * FROM t_enviro WHERE timestamp > %s;' %int(getTimeStampDay(dateFrom)))    
    else:
        logging.debug("Extracting all data")
        queryString = ('SELECT * FROM t_enviro')    

    logging.debug('Reading EnviroDB %s ' %__file__)
    logging.debug("sql script %s",queryString)
    dbConn = getConnection()
    dbCursor = getConnection().cursor()

    # 
    # The result of a "cursor.execute" can be iterated over by row
    # timestamp,pressure,pm2_5,pm10,noise,humidity,temperature,pm1) 
    for row in dbCursor.execute(queryString):
        logging.info("TimeStamp %s" %getTimeFromTimeStamp(row[0]))
        logging.info("Pressure %s" %str(row[1]))
        logging.info("pm2_5 %s" %str(row[2]))
        logging.info("pm10 %s" %str(row[3]))
        logging.info("noise %s" %str(row[4]))
        logging.info("humidity %s" %str(row[5]))
        logging.info("temperature %s" %str(row[6]))
        logging.info("pm1 %s" %str(row[7]))


   


 
