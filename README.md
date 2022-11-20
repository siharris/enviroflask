# enviroflask
Enviromental Logging Service for Enviro Urban Pico PI

Enviro pico recorder  is for hosting a simple service to receive the 
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
