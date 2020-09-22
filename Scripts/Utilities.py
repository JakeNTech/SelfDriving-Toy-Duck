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
def get_parameters():
	parameters = {
		"duckParameters": {
			'width': "320",
			'height': "240",
			'pigame': "False",
			'verbose': "True",
			'channels': "3",
			#GPIO Pinout
			'duckConfiguration': {
				"FORWARD": {"pin":11,"lable_code":0},
				"RIGHT": {"pin":13, "lable_code":1},
				"LEFT": {"pin":15, "lable_code":2},
				"BACKWARDS": {"pin":18, "lable_code":-1},
				"SPEED":{"pin": 16, "default":55}
			}
		}
		,'cameraParameters':{
			'width': "320",
			'height': "240"
		}
		,'webserverParameters':{
			'port': "8090",
			'duck': None
		}
	}
	parameters['headParameters'] = {
		"model": "/home/pi/SelfDriving-Toy-Duck/keras_model_0.01_learning_rate_32_batch_size_SGD_optimizer_89.0_acc.model",
	}
	return parameters