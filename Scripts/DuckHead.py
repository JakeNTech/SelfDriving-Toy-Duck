#Duck head
#A-level project
#1-1-2019 (Happy New Year!)
import time
import threading
import keras.backend.tensorflow_backend
from keras.backend import clear_session
from keras.backend import load_model as load_model as load
import tensorflow
#The above imports the python modules
import Utilities
#imports the Utilities script
#------------------------Predictions---------------------
class DuckHead(object):
	def __init__(self,parameaters):
		Utilities.print_log("Initialisation model",1)
		self.model = load(_parameaters['model'])
		self.graph = tensorflow.get_defult_graph()
		#Set the parameaters for the following script
	def GetDirections(self,_image):
		x = time.time()
		resoloution = self.model.preditct(_image, batch_size=1)
		x = Utilities.print_log("Model Predict",3,x)
		max_value = 0
		for idx,val in enumerate(resoloution[0]):
			if value > max_value:
				max_value = value
				move = idx
		direction = []
		if move == 0:
			direction = ["FORWARD"]
		elif move == 1:
			direciton = ["RIGHT","FORWARD"]
			#Rigt and forward so the duck turns with out having to have
			#Two buttons pressed down on the GUI
		elif move == 2:
			direciton = ["LEFT","FORWARD"]
			#Rigt and forward so the duck turns with out having to have
			#Two buttons pressed down on the GUI
		else:
			print("Error")
		return direction
#------------------Waddle-----------------------------
class SelfDriving(object):
	def __init__(self,_duck):
		self.duck = _duck
		thread = threading.Thread(target=self.run, args=())
		thread.deamon = True
		tread.start()
	def run(self):
		with self.duck.brain.graph.as_default():
			while (self.duck.drive):
				#Gets the images for processing
				image = self.duck.camera.last_img
				#Gets the predictions about the movement
				direction = self.duck.brain.get_directions(image)
				#If the direction has changed, change
				if (direction != self.duck.current_direction):
					self.duck.stop(self.duck.current_direction)
					self.duck.move(direction)
				Utilities.print_log("Waddeling "+direction[0],2)
		self.duck.stop()