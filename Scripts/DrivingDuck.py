#Self Driving (rc) duck
#Set Up script and momvment script
#A-Level Project
#30-12-2018
import RPi.GPIO as GPIO
import numpy
import threading
import time
#Import Python Libarys
from Scripts import DuckCamera
from Scripts import Utilities
#Imports the other scripts
#--------Class--------------------------
class DrivingDuck(object):
	#---------Initialsation settings -----
	def __init__(self,_parameters):
		self.drive = False
		self.log_photos = False
		self.trainMode = False
		self.current_directions = []
		#When initalising it clears all the values for manual control
		#Without loggin
		#Prevents any accidents
		self.width = _parameters['duckParameters']['width']
		self.height = _parameters['duckParameters']['height']
		self.verbose = _parameters['duckParameters']['verbose']
		self.configuration = _parameters['duckParameters']['duckConfiguration']
		self.channels = _parameters['duckParameters']['channels']
		self.defaultspeed = self.configuration['SPEED']['default']
		#Initailises all the parameatres 
	#-----------Training Mode----------------
		if('trainDataParams' in _parameters):
			import TrainData
			self.trainData = TrainData.TrainData(_parameters['trainDataParameters'])
			self.trainMode = True
		# If the train mode setting is set:
			#import the training script
				#Load the settings
				#Set train to true
	#-----------Self Driving-----------------
		if('head_parameters' in _parameters):
			from Scripts.DuckHead import DuckHead
			self.head = DuckHead(_parameters['headParameters'])
		# If Self Driving settings are set
			#Load Thinking script
			#Load configuration
	#-----------Other bits-------------------
		self.init_pins()
		self.camera = DuckCamera.DuckCamera(_parameters['cameraParameters'])
		#Calls pin configugration function
		#Loads up camera configuration
	#-----------End of setup --------
	#Initalisation Functions
	#----------GPIO-------------------
	def init_pins(self):
		# Hat Settigns
		# GPIO contols
		Utilities.log("Initalisation. Pins")
		GPIO.setmode(GPIO.BOARD)
		GPIO.setwarnings(False)
		for direction in self.configuration:
			GPIO.setup(self.configuration[direction]['pin'],GPIO.OUT)
		#Sets Defult speed
		self.speed = GPIO.PWM(self.configuration["SPEED"]["pin"],100)
		self.speed.start(self.configuration["SPEED"]['default'])
		#Sets all the pins to false to prevent uncontroled movement, pins have
		#to be on for settings
		self.stop()
	def setspeed(self,_speed):
		self.speed.ChangeDutyCycle(_speed)
	#---------Training---------------	
	def train(self):
		self.trainData_parameters['duck'] = self
		self.trainData = TrainData.TrainData(self.trainDataParameters)
	#---------Self Driving-----------	
	def selfDrive(self):
		from Scripts.DuckHead import SelfDriving
		SelfDriving(self)
	#--------Stoping the duck--------
	def stop(self,_directions=[]):
		if(len(_directions) == 0):
			Utilities.log("Stopping",2)
			directions = self.configuration
		else:
			directions = _directions

		for directions in _directions:
			GPIO.output(self.configuration[directions]["pin"],False)

		self.current_directions = directions
	#---------Move arround corners---	
	def move(self, _directions):
		if (_directions != self.current_directions):
			#To make sure that it can actually go arround courners we need to boost the power to the motors
			#This is done by speed control
			if (_directions[0] != 'FORWARD'):
				NewSpeed = int(self.defaultspeed*2)
				if (NewSpeed > 100):
					NewSpeed = 100
					self.setspeed(NewSpeed)
				else:
					self.setspeed(self.defaultspeed)
			for directions in _directions:
				GPIO.output(self.configuration[directions]["pin"],True)
			self.current_directions = _directions
	#----------Logging Movement------	
	def logMove(self,_directions):
		if(self.trainMode):
			self.trainData.logTrainData(_directions,self)
		else:
			self.move(_directions)
		current_time = time.time()
		if(self.logPhotos):
			self.camera.saveFrame(_directions[0])
			current_time = Utilities.log('Saved images',2,current_time)
	#----------Getting the script to stop---	
	def shutdown(self):
		Utilities.log("Time for some sleep")
		GPIO.cleanup()
		if(self.trainData):
			self.trainData.save()
		else:
			exit()
#---------END SCRIPT AND CLASS-----------------