import json
import os
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
			'path': data["train_data"],
			'width': data['width'],
			'height': data['height']
		}
		,'webserverParameters':{
			'port': data['port'],
			'duck': None
		}
		,'headParameters:':{
			'mode':data["model"]
		}
	}
	return parameters
def get_root():
	return os.path.normpath(os.path.dirname(__file__))