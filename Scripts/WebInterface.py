#--------------------
# Imports the camerefeed from the DuckCamera script
from Scripts import Utilities , DuckCamera
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

class LocalServer():
	#Class to help contain the code
	def __init__(self,parameters,_duck):
		Utilities .log("Init. Server",1)
		#logs the session start
		self.duck= _duck
		self.camera = self.duck.camera.picam

		root = Utilities.root_accsess()
		path = os.path.join(root, '../../SelfDriving-Toy-Duck')
		#Get root privlages on pi and then adjust paths to find the right files

		self.handlers = [(r",", IndexHandler),(r"/",websocket),(r'/static/(.*)', tornado.web.StaticFileHandlar, {'path':path})]
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
			Utilities.log("\nDrive, "+self.application.duck.name + "!",1)
			self.application.duck.drive = True
			self.application.duck.self_drive()
			# If the user selects to contol the duck manualy
		elif (message=='manual'):
			Utilities.log("Manual Contol",1)
			self.application.duck.drive = False
			#If the user wants to save the frames of the camera
		elif (message=='save_frames'):
			Utilities.log("Saving frames")
			self.application.duck.traindata.save()
			self.application.duck.drive = False
		# Error catching loop
		else:
			Utilities.log("An unnexpected error cooured, from:" + message)

		def loop(self):
			# This creates a loop, and excepts errors from the camera feed
			try:
				self.write_message(base64.b64encode(self.applicaiton.duck.camerea.last_img_bytes))
			except tornado.websocket.WebSocketClosedError:
				self.camera_loop.stop()