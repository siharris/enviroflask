"""
Enviro pico recorder version 1.0 is for hosting a simple service to receive the 
posts from the pimironi  enviro urban (Pico W board) . As an alternative to MQTT, 
Adafruit IO, InfluxDB this provides a custom HTTP endpoint. This very simple flask
application in its current version does not have any authentication or configuration 
files. Its designed to work with a single pico but it would be easy to expand this 
by adding the nickname to differentiate multiple devices which it can then save to 
the sqlite database. 

Use the envirodbcreate.py to instiate the database before using . The easiest way to 
run this is to:-

      $ nohup runflask.sh &

The database and log file will be written to the local working directory.  There are 
callable rest functions :-

/post this takes the call from the enviro urban and stores it with a timestamp . Please
note this will get renamed in the next version. 

/query this can be used to retrieve a data range , if no paramters are passed it will
 just provide a count of the number of records. If paramters are the response will come
 back in json. 

Further enhancements to this are planned for version 2.0 they will include :-

1) Pluggable authentication mechanism 
2) Method name change for posts
3) Support for multiple enviro urbans 
4) COnfig file to specificy locations and names 
5) Swagger generated documentation 
6) Improved error handling 
7) Configure the service port to be configured , current default is port 5000

"""

from flask import Flask
from flask import jsonify, request
from datetime import datetime

import logging
import sys
import os.path
import sqlite3




app = Flask(__name__)
__author__ = 'simond4'
DATABASE = "enviro.db"


logging.basicConfig(filename='envirorecorder.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')


@app.route("/posts/", methods=['POST'])
def record():
    """ Records the Enviro Urban post 

    Parameters 
    ----------

    Receives a JSON payload 


    """
    try:
        content_type = request.headers.get('Content-Type')
        if (content_type == 'application/json'):
            app.logger.info('Recording sensor reading')
            jsonResult = request.get_json()

            app.logger.debug("received reading from nickname %s" %jsonResult["nickname"])
            readings = jsonResult["readings"]
            for key,value in readings.items():
                app.logger.debug("key %s value %s" %(key,value))
                
    
            pressure = readings["pressure"]
            pm2_5 = readings["pm2_5"]
            pm10 = readings["pm10"]
            noise = readings["noise"]
            humidity = readings["humidity"]
            temperature = readings["temperature"]
            pm1 = readings["pm1"]
            timestampRaw = jsonResult["timestamp"]
            timestamp = getTimeStamp(timestampRaw)


            dbConn = getConnection()
            dbCursor = getConnection().cursor()
        
            try:        
                with dbConn: 
                    sql = ''' INSERT INTO t_enviro(timestamp,pressure,pm2_5,pm10,noise,humidity,temperature,pm1) VALUES(?,?,?,?,?,?,?,?) '''
                    result = dbCursor.execute(sql,(timestamp,pressure,pm2_5,pm10,noise,humidity,temperature,pm1))
                    app.logger.debug("Insert to DB executed result %s" %result)

            except:
                app.logger.error("Unable to update database %s" %sys.exc_info()[0])
                return jsonify({"failure": "Unable to record reading check server log"})

        return jsonify({"success": "Successfully recorded reading."})

    except Exception as e: 
        logging.debug(e)

@app.route('/query', methods=['GET'])
def query():
    """
    
    Parameters 
    ----------

    Takes dateFrom=


    Returns
    -------

    """
    args = request.args
    if len(args) == 0:
        return jsonify(getReadingsCount())
    else:
        dateFrom = request.args.get('dateFrom')
        dateTo = request.args.get('dateTo')
        return jsonify(getReading(dateFrom,dateTo))
        

   
       
def getDatabaseFilePath():
    return "%s//%s"% (os.getcwd() , DATABASE )
        

def getReadingsCount():
    """ Gets the number of record in the sqlite database

    Returns 
    -------

    returns a count of the number of records 
    
    """
    
    queryString = ('SELECT count(*) FROM t_enviro')    
    logging.debug('Reading EnviroDB %s ' %__file__)
    logging.debug("sql script %s",queryString)

    dbCursor = getConnection().cursor()
    dbCursor.execute(queryString)
    row = dbCursor.fetchone()
    count = row[0]
    result = {"count":str(count)}
    return result

def getReading(dateFrom,dateTo):
    """ Gets Reading from sqlite database 

    Parameters
    ----------

    dateFrom : str in yyyymmdd format e.g. 20221111
    dateTo : str in yyyymmdd format e.g. 20221112
    
    Returns 
    -------

    returns a dictionary 

    """
    try:
        queryString = "SELECT * FROM t_enviro WHERE timestamp >= {} AND timestamp <= {};".format(getTimeStampDay(dateFrom),getTimeStampDay(dateTo))     
        logging.debug('Reading EnviroDB %s ' %__file__)
        logging.debug("sql script %s",queryString)
        dbCursor = getConnection().cursor()
        dbCursor.execute(queryString)
            
        cnt=0
        result = {}
        for row in dbCursor.execute(queryString):
            result[cnt] = {"TimeStamp": getTimeFromTimeStamp(row[0]) , "Pressure": str(row[1]),"pm2_5" : str(row[2]) ,"pm10" : str(row[3]) ,
            "noise" : str(row[4]), "humidity" : str(row[5]),"temperature" :str(row[6]),"pm1" : str(row[7])}
            cnt=cnt+1
        return result

    except Exception as e:
        logging.error(e)


def getConnection():

    conn = sqlite3.connect(getDatabaseFilePath(), isolation_level=None) 
    return conn

def getTimeStamp(timeStampString):

    timeStamp = datetime.strptime(timeStampString, "%Y-%m-%d %H:%M:%S").timestamp()
    app.logger.debug('Current timestamp %s' %timeStamp)
    return timeStamp

def getTimeFromTimeStamp(timeStamp):

    timeStamp2 = datetime.fromtimestamp(timeStamp)
    timeStamp2.strftime('%Y-%m-%d %H:%M:%S')
    app.logger.debug('Returning normal time from timestamp %s' %timeStamp2)
    return timeStamp2

def getTimeStampDay(timeStampString):

    timeStampDay = datetime.strptime(timeStampString, "%Y-%m-%d").timestamp()
    app.logger.debug('Current timestamp %s' %timeStampDay)
    return str(int(timeStampDay))

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000)