#Project Self-Driving (toy) Duck
#Utilities.py
import argparse
import time
import json
import os
#import the needed modules

def log(_message,_ident=0,_time=0):
	indent = " "*_ident
	if (_time!= 0):
		ti = time.time() - _time
		if (ti > 60):
			ti = round(ti/60,2)
			units = "minutes"
		elif (ti > 3600):
			ti = round(ti/3600,2)
			units = "hours"
		else:
			units = "seconds"
		print(("%s %s. Time: %s %s ")%(indent,_message,ti,units))
# The above function is for making the log, printing it to the console,
#Indents, prints the message, and then the time and the unit of time
def wait(_time):
	time.sleep(_time)
#This function does what it says on the tin, its called when sleep is needed
def epoch():
	return str(int(time.time()))
#This function is a UNIX time system, counts the number of seconds
#that have gone since starting
#MUST BE RETURNED AS A STRING
def ms_epoch():
	return (int(datetime.datetime.utcnow() - datetime.datetime(1970,1,1)).total_seconds() * 1000)
#This function gets the time form a windows based system or systems where
#standerd epoch doesn't work
def root_accsess():
	return os.path.normpath(os.path.dirname(__file__))
#This get root privaleges, the second highest you can get on UNIX
#It goes under SU rights
#This converts the command line arguments into a way python will understand
def get_parameters():
	with open("./Config/configuration.json") as file:
		data = json.load(file)
	# this opens the configuration file that contains information such as the 
	#the GIPO pins
	#Below is setting the setings for the duck
	parameters = {
		"duckParameters": {
			'width': data['width'],
			'height': data['height'],
			'pigame': data["pigame"],
			'verbose': data["verbose"],
			'channels': data["channels"],
			'duckConfiguration': data['duckConfiguration']
		}
		,'cameraParameters':{
			'width': data['width'],
			'height': data['height']
		}
		,'webserverParameters':{
			'port': data['port'],
			'duck': None
		}
		,'headParameters:'{
			'mode':data["model"]
		}

	}
	return parameters