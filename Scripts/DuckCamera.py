#Duck Camera
#Project Duck
#--------------------
from Scripts import Utilities 
#Imports the Utilities script
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
		Utilities.log("Init. Camera")

		self.stream = True
		self.path = _parameters['path']
		#Tells other scrips about the camerea
		self.picam = PiCamera()
		self.picam.rotation = 180
		self.picam.framerate = 15
		self.picam.resolution = (_parameters['width'], _parameters['height'])
		# This sets the rotation and resoloutin of the camera.
		time.sleep(2)
		#this allows for the camera to sort its self out in tearms of expouser
		#and contrast, and fous. This also factors in the delays
		def save_frame(self,_turn):
			name = string(Utilities.ms_ephoc())+":"+string(_turn)
			#This takes the movement name ie.left and converts it to text
			#This allows for training

#Getting the camera feed
#NO TWITCH
class CameraFeed(object):
	def __init__(self,_duck):
		self.duck = _duck
		self.camera = self.duck.camera
		thread = threading.Thread(target=self.run, args=())
		thread.deamon = True
		thread.start()
		#This creates a thread for the camera feed
	def run(self):
		self.detection = ObjectDetection()
		while (self.camera.stream):
			raw_capture = picamera.array.PiRGBArray(self.camera.picam)
			self.camera.picam.capture(raw_capture, format="rgb",use_video_port=True)
			#this creates a RGB capture and files it into an array

			img = self.detection.detect(raw_capture.array.astype('uint8'))
			# this runs the object detection
			self.camera.stop_detected = self.detection.stop_detected

			image_array = numpy.zeros([1,240,320,3])
			image_array[0]= img
			self.camera.last_img = image_array
			#Saves the current image/frame being used and displayed
			
			img = Image.fromarray(img.astype("uint8"),mode="RGB")
			f = io.BytesIO()
			img.save(f, "JPEG")
			self.camera.last_img_bytes = f.getvalue()
			#This converts the image into its raw btes value and then saves it
class ObjectDetection(object):
	def __init__(self):
		self.stop_detected = False
		self.classifier = cv2.CascadeClassifier('Config/stop_sign.xml')

	def detect(self, _image):
		# detection
		cascade_obj = self.classifier.detectMultiScale(
			_image,
			scaleFactor=1.1,
			minNeighbors=5,
			minSize=(30, 30),
			flags=cv2.CASCADE_SCALE_IMAGE
		)

		# draw a rectangle around the objects
		if (len(cascade_obj)):
			self.stop_detected = True
			for (x_pos, y_pos, width, height) in cascade_obj:
				cv2.rectangle(_image, (x_pos+5, y_pos+5), (x_pos+width-5, y_pos+height-5), (255, 255, 255), 2)
				cv2.putText(_image, 'STOP', (x_pos, y_pos-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)			
		else:
			self.stop_detected = False

		return _image
		#This finds an object from the model file and puts a box arround it
		#It could be made to put text under the object that has been detected, this 
		#will be seen by the end user on the HTML page