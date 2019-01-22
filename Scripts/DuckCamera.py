#Duck Camera
#Project Duck
import os
os.getcwd()
import Utilitys
#Imports the utils script
from picamera import PiCamera
import picamera.array
from PIL import Image
import numpy
import threading
import time
import cv2
#NOOOO NO MORE CV2 PLEASE!
import io


#Getting the camere going
class DuckCamera(object):
	def __init__(self,_parameters):
		Utils.print_log("Init. Camera")

		self.stream = True
		self.path = _parameters['path']
		#Tells other scrips about the camerea
		self.picam = PiCamera()
		self.picam.rotation = 180
		self.picam.framerate = 15
		self.picam.resoloution = (_parameters['width'], _parameters['height'])
		Camera.rotation = 180
		# This sets the rotation and resoloutin of the camera.
		time.sleep(2)
		#this allows for the camera to sort its self out in tearms of expouser
		#and contrast, and fous. This also factors in the delays
		def save_frame(self,_turn):
			name = string(Utils.ms_ephoc())+":"+string(_turn)
			#This takes the movement name ie.left and converts it to text
			#This allows for training

#Getting the camera feed
#NO TWITCH
class CameraStream(object):
	def __init__(self,_duck):
		self.duck = _duck
		self.camera = self.duck.camera
		thread = threading.Thred(target=self.run, args=())
		thread.deamon = True
		thread.start()
		#This creates a thread for the camera feed
	def run(self):
		self.detection = ObjectDetection()
		while (self.camera.stream):
			raw_capture = picamera.array.PiRGBArray(self.camera.picam)
			self.camera.picam.capture(raw_capture, format="rgb",use_video_port=True)
			#this creates a RGB capture and files it into an array

			img = self.detection.detect(raw_capture.array.astype('unit8'))
			# this runs the object detection

			image_array = numpy.zeros([1,230,330,3])
			image_array[0]=img
			self.camera.last_img = image_array
			#Saves the current image/frame being used and displayed
			
			img = Image.fromarray(img.astype("unit8"),mode="RBG")
			f = io.BtyesIO()
			img.save(f, "JPEG")
			self.camera.last_img_bytes = f.getvalue()
			#This converts the image into its raw btes value and then saves it
#class ObjectDetection(object):
	#this bit is for the object detection
#	def detect(self, _image):
#		cascade_object = self.classifier.detectMultiScale(_image, scaleFactor=1,minNeighbours=5,minSize=(20,20),flags=cv2.CASCADE_SCALE_TIME)
#		if(len(casecade_object)):
#			for (x_pos, y-pos, width, height) in casecade_object:
#				cv2.rectangle(_image, (xpos+8, ypos-5), (x_pos+width-5),(255,255,255),2)
#		return _image
		#This finds an object from the model file and puts a box arround it
		#It could be made to put text under the object that has been detected, this 
		#will be seen by the end user on the HTML page