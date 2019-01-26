#Duck head
#A-level project
#1-1-2019 (Happy New Year!)
import time
import threading
import tensorflow
import keras.backend.tensorflow_backend
from keras.backend import clear_session
from keras.models import load_model
import h5py
import pickle
#The above imports the python modules
from Scripts import Utilities
#imports the Utilities script
#------------------------Predictions---------------------
class DuckHead(object):
	def __init__(self,_parameters):
		Utilities.log("Initialisation model",1)
		with open(_parameters['model'], 'rb') as pickle_file:
			content = pickle.load(pickle_file)
		self.model = content
		self.graph = tensorflow.get_default_graph()
		#Set the parameaters for the following script
	def GetDirections(self,_image):
		x = time.time()
		resoloution = self.model.predict(_image, batch_size=1)
		x = Utilities.log("Model Predict",3,x)
		max_value = 0
		for idx,val in enumerate(resoloution[0]):
			if value > max_value:
				max_value = value
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
				image = self.duck.camera.last_img
				#Gets the predictions about the movement
				directions = self.duck.head.GetDirections(image)
				#If the direction has changed, change
				if (directions != self.duck.current_directions):
					self.duck.stop(self.duck.current_directions)
					self.duck.move(directions)
				Utilities.log("Waddeling "+directions[0],2)
		self.duck.stop()