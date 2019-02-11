#Project Self-Driving (toy) Duck
#DuckHead.py
#1-1-2019 (Happy New Year!)
import time
import threading
import keras.backend.tensorflow_backend
from keras.backend import clear_session
from keras.models import load_model
import tensorflow as tf
import h5py
import pickle
#The above imports the python modules
from Scripts import Utilities
#imports the Utilities script
#------------------------Predictions---------------------
class DuckHead(object):
	def __init__(self,_parameters):
		Utilities.log("Initialisation model",1)
		path = "/home/pi/SelfDriving-Toy-Duck/Config/keras_model_0.01_learning_rate_32_batch_size_SGD_optimizer_89.0_acc.model"
		self.model = load_model(path)
		#with open(_parameters['model'],'rb')as file:
		#	NewFile = Unpickler(file).load()
		#self.model = NewFile
		self.graph = tf.get_default_graph()
		#Set the parameaters for the following script
	def GetDirections(self,_image):
		x = time.time()
		resoloution = self.model.predict(_image, batch_size=1)
		x = Utilities.log("Model Predict",3,x)
		max_val = 0
		for idx,val in enumerate(resoloution[0]):
			if val > max_val:
				max_val = val
				move = idx
		directions = []
		if move == 0:
			directions = ["FORWARD"]
		elif move == 1:
			directions = ["RIGHT","FORWARD"]
			#Rigt and forward so the duck turns with out having to have
			#Two buttons pressed down on the GUI
		elif move == 2:
			directions = ["LEFT","FORWARD"]
			#Rigt and forward so the duck turns with out having to have
			#Two buttons pressed down on the GUI
		else:
			print("Error")
		return directions
#------------------Waddle-----------------------------
class SelfDriving(object):
	def __init__(self,_duck):
		self.duck = _duck
		thread = threading.Thread(target=self.run, args=())
		thread.deamon = True
		thread.start()
	def run(self):
		with self.duck.head.graph.as_default():
			while (self.duck.drive):
				#Gets the images for processing
				image = self.duck.camera.lastImg
				#Gets the predictions about the movement
				directions = self.duck.head.GetDirections(image)
				#If the direction has changed, change
				if (directions != self.duck.currentDirections):
					self.duck.stop(self.duck.currentDirections)
					self.duck.move(directions)
				Utilities.log("Waddeling "+directions[0],2)
		self.duck.stop()