#--------------------
# Imports the camerefeed from the DuckCamera script
import Utilitys
#Import the utilitys script
import time
import os
import io
import base64
import webbrowser
import threading
# Imports all the needed buit in python moduls
from tornado.ioloop import PeriodicCallback
import tornado.websocket
import tornado.web
# Imports Tornado Modules
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
class LocalServer():
	#Class to help contain the code
	def __init__(self,params,_duck):
		Utils.print_log("Init. Server",1)
		#logs the session start
		self.duck= _duck
		self.camera = self.duck.camera.picam

		root = Utils.set_root()
		path = os.path.join(root, '../../SelfDriving-Toy-Duck')
		#Get root privlages on pi and then adjust paths to find the right files

	def stream(self):
		settings = {'debug':True}
		super(LocalServer,self).__init__(self.handlers, **settings)
		CameraStream(self.duck)
		self.listen(self.port)
		tornado.ioloop.IOLoop.instance().start()
		#This starts the camera stream for the duck, and users a pre-defined loop
class WebSocket(tornado.websocket.WebSocketHandler):
	def on_message(self, message):
		#This starts an infinate loop when its called up
		if message == "Start camera":
			if not self.application.requier_login or self.get_secure_cookie(self.application.cookie):
				self.camera_loop = PeriodicCallBack(self.loop, 150)
				self.camera_loop.start()
				#This sets the camera to 15 Frames per second
				# It also makes a loop that will keep the camera stream alive
			else:
				print("Unknown error")
		elif (message in {"BACk","FORWARD","LEFT","RIGHT"}):
			direction = [message]
			# This set the direction to the variable message that is being passed across
			if (message in ["LEFT","RIGHT"]):
				direction = [message,"BACK"]
				#If the user is pressing right or left the duck still needs to go forward
			elif (self.application.duck.train):
				self.application.duck.log_and_move(directions)
				# if the duck is in train mode it logs 
			else: 
				self.application.car.move(direction)
				#This makes it carry on as normal

		#Stopping the duck
		elif (message[5:] in ["BACK","FORWARD","RIGHT","LEFT"]):
			self.application.duck.stop()
			#If user has pressed the self drive button
		elif (message == 'self_drive'):
			Utils.print_log("\nDrive, "+self.application.duck.name + "!",1)
			self.application.duck.drive = True
			self.application.duck.self_drive()
			# If the user selects to contol the duck manualy
		elif (message=='manual'):
			Utils.print_log("Manual Contol",1)
			self.application.duck.drive = False
			#If the user wants to save the frames of the camera
		elif (message=='save_frames'):
			Utils.print_log("Saving frames")
			self.application.duck.traindata.save()
			self.application.duck.drive = False
		# Error catching loop
		else:
			Utils.print_log("An unnexpected error cooured, from:" + message)

		def loop(self):
			# This creates a loop, and excepts errors from the camera feed
			try:
				self.write_message(base64.b64encode(self.applicaiton.duck.camerea.last_img_bytes))
			except tornado.websocket.WebSocketClosedError:
				self.camera_loop.stop()