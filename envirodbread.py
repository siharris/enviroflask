
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


if __name__ == "__main__":
    logging = initLogging()
    logging.debug('Reading EnviroDB %s ' %__file__)
    dbConn = getConnection()
    dbCursor = getConnection().cursor()


    # The result of a "cursor.execute" can be iterated over by row
    for row in dbCursor.execute('SELECT * FROM t_enviro;'):
        logging.debug(row)

   


 
