#Project Self-Driving (toy) Duck
#Utilities
import datetime
import argpase
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
			units = "m"
		elif (ti > 3600):
			ti = round(ti/3600,2)
			units = "h"
		else:
			units = "s"
		print(("%s %s. Time: %s %s ")%(indent,_message,ti,unit))
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
	return os.path.normpath(os,path.dirname(__file__))
#This get root privaleges, the second highest you can get on UNIX
#It goes under SU rights
def get_arguments();
	parser = argpase.ArgumentsParser(prog="drive")
	parser.add_arguments("-train",help="Set if wanting to use train mode", action="store_true", defult=False)
	prased_args = parser.parse_args()
	return prased_args
#This converts the command line arguments into a way python will understand
def get_parameters(_train):
	with open("config/config.json") as file:
		data = json.load(file)
	# this opens the configuration file that contains information such as the 
	#the GIPO pins
	#Below is setting the setings for the duck
	params = {
		"duck_params": {
			'width': data['width'],
			'hight': data['height'],
			'name': data['title'],
			'pigame': data["pigame"],
			'verbose': data["verbose"],
			'channels': data["channels"],
			'duck_config': data['duck_config']
		}
		,'camera_params':{
			'path': data["train_data_stoage"],
			'width': data['width'],
			'height': data['height']
		}
		,'webserver_params':{
			'port': data['port'],
			'duck': None
		}
	}
	if(_train):
		# if the train mode is enabled then use thease parameaterts
		params['train_data_params']= {
			'path': data['train_data_storage'],
			'width': data['width'],
			'height': data['height'],
			'channels':data:['channels']
		}
	else:
		# if not in training mode set to use the model file
		params['head_params'] = {
			"model": data["model"]
		}
	return params