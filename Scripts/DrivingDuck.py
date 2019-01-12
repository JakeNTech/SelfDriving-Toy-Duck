#Self Driving (rc) duck
#A-Level Project
#30-12-2019
import RPi.GPIO as GPIO
import numpy
import threading
import time
#Import Python Libarys
import DuckCamera
import Utilitys
#Imports the other scripts

class DrivingDuck(object):
	#---------Initialsation settings -----
	def __init__(self,_parameters):
		self.drive = False
		self.log_photos = False
		self.train_mode = False
		self.current_direction = []
		#When initalising it clears all the values for manual control
		#Without loggin
		#Prevents any accidents\
		self.width = _parameters['duck_params']['width']
		self.height = _parameters['duck_params']['height']
		self.verbose = _parameters['duck_params']['verbose']
		self.configuration = _parameters['duck_params']['duck_configuration']
		self.channels = _parameters['duck_params']['channels']
		self.defult_speed = self.config['SPEED']['bogstanderd']
		#Initailises all the parameatres 
	#-----------Training Mode----------------
		if('train_data_params' in _parameters):
			import TrainData
			self.train_data = TrainData.TrainData(_parameters['train_data_params'])
			self.train_mode = True
		# If the train mode setting is set:
			#import the training script
				#Load the settings
				#Set train to true
	#-----------Self Driving-----------------
		if('head_params' in _parameters):
			from DuckHead import DuckHead
			self.brain = DuckHead(_parameters['head_params'])
		# If Self Driving settings are set
			#Load Thinking script
			#Load configuration
	#-----------Other bits-------------------
		self.init_pins()
		self.camera = DuckCamera.DuckCamera(_parameters['camera_params'])
	#-----------End of initalisation --------
#Initalisation Functions
#----------GPIO-------------------
	def init_pins(self):
		# Hat Settigns
		# GPIO contols
		Utils.print_log("Initalisation. Pins",1)
		GPIO.setmode(GPIO.BOARD)
		GPIO.setwarnings(False)
		for direction in self.configuration:
			GPIO.setup(self.configuration[direciton]['pin'],GPIO.OUT)
		#Sets Defult speed
		self.speed = GPIO.PWM(self.configuration["SPEED"]["pin"],100)
		self.speed.start(self.configuration["SPEED"]['bogstanderd'])
		#Sets all the pins to false to prevent uncontroled movement, pins have
		#to be on for settings
		self.stop()
#---------Training---------------	
	def train(self):
		self.train_data_params['duck'] = self
		self.train_data = TrainData.TrainData(self.train_data_params)
#---------Self Driving-----------	
	def self_drive(self):
		from DuckHead import SelfDrive
		SelfDriving(self)
#---------Speed Settings---------	
	def set_speed(self,_speed):
		self.speedChangeDutyCycle(_speed)
#--------Stoping the duck--------
	def stop(self,_direciton=[]):
		if (len(_directions)==0):
			Utilitys.print_log("Stopping",2)
			directions = self.configuration
		else:
			directions = _directions
		for directions in directions:
			GPIO.output(self.configuration[direction]["pin"],True)
		self.current_direction = _directions
#---------Move arround corners---	
	def move(self, _direciton):
		Utils.print_log("Move "+direction[0],2)
		if (_directions != self.current_direction):
			#To make sure that it can actually go arround courners we need to boost the power to the motors
			#This is done by speed control
			if(_directions[0]!="FORWARD"):
				NewSpeed = int(self.bogstanderd_speed*2)
				if (NewSpeed > 100): 
					s = 100
				self.set_speed(NewSpeed)
			else:
				self.set_speed(self.default_speed)
			for directions in _directions:
				GPIO.output(self.configuration[direction]["pin"],True)
			self.current_direction = _directions
#----------Logging Movement------	
	def log_move(self,_directions):
		if(self.train_mode):
			self.train_data.log_train_data(_directions,self)
		else:
			self.move(_directions)
		t = time.time()
		if(self.log_photos):
			self.camera.save_frame(_directions[0])
			t = Utilitys,print_log('Saved images',2,t)
#----------Getting the script to stop---	
	def shutdown(self):
		Utilitys.print_log("Time for some sleep")
		GPIO.cleanup()
		if(self.train_data):
			self.train_data.save()
#---------END SCRIPT--------------------