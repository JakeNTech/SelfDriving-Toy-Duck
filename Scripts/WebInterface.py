#Project Self-Driving (toy) Duck
#WebInterface.py
#-----LOCAL IMPORTS-----------------------
from Scripts import Utilities
from Scripts.DuckCamera import CameraFeed
from Scripts import DrivingDuck
#-----IMPORTS External scripts-------------
import time
import os
import io
import base64
import webbrowser
import threading
from tornado.ioloop import PeriodicCallback
import tornado.websocket
import tornado.web
#------CLASS Giving tornado the file paths---------
class LocalServer(tornado.web.Application):
	#Class to help contain the code
	def __init__(self,parameters,_duck):
		Utilities .log("Init. Server",1)
		#logs the session start
		self.duck= _duck
		self.camera = self.duck.camera.picam
		self.port = parameters['port']
		#Get root privlages on pi and then adjust paths to find the right files
		root = Utilities.root_accsess()
		path = os.path.join(root, '../../SelfDriving-Toy-Duck')
		#Sets the file paths for the Index and lets tornado know we are using its file management
		self.handlers = [(r"/", IndexHandler),(r"/websocket",WebSocket),(r'/static/(.*)', tornado.web.StaticFileHandler, {'path':path})]
	def stream(self):
		settings = {'debug':True}
		super(LocalServer,self).__init__(self.handlers, **settings)
		CameraFeed(self.duck)
		self.listen(self.port)
		tornado.ioloop.IOLoop.instance().start()
		#This starts the camera stream for the duck, and users a pre-defined loop
#------CLASS IndexHandler --------------------
class IndexHandler(tornado.web.RequestHandler):
	#When you type in the IP/URL you are taken to an Index.html by defualt
	#This is the handler for that in tornado
	def get(self):
		self.render("../WebServer/index.html", port=self.application.port)
class ErrorHandler(tornado.web.RequestHandler):
	#if there is anerror this is what tornado should send
	def get(self):
		self.send_error(status_code=403)
#Class The Coms Between the GUI and the Scripts ---
class WebSocket(tornado.websocket.WebSocketHandler):
	def loop(self):
		#this creates a loop for the camera to start running on
		try:
			self.write_message(base64.b64encode(self.application.duck.camera.lastImgBytes))
		except tornado.websocket.WebSocketClosedError:
			self.cameraLoop.stop()
	def on_message(self, message):
		#This starts an infinate loop when its called up
		if message == "readCamera":
			self.cameraLoop = PeriodicCallback(self.loop, 150)
			self.cameraLoop.start()
			#This sets the camera to 15 Frames per second
			# It also makes a loop that will keep the camera stream alive
		elif message == "shutdown":
			self.DrivingDuck.shutdown()
		elif (message in ["BACKWARDS","FORWARD","LEFT","RIGHT"]):
			directions = [message]
			# This set the direction to the variable message that is being passed across
			if (message in ["LEFT","RIGHT"]):
				directions = [message,"FORWARD"]
			self.application.duck.move(directions)
			#This makes it carry on as normal
		#Stopping the duck
		elif (message[5:] in ["BACKWARDS","FORWARD","RIGHT","LEFT"]):
			self.application.duck.stop()
			#If user has pressed the Start Self-Drive  button
		elif (message == 'SelfDrive'):
			Utilities.log("\n Self Drive!",1)
			self.application.duck.drive = True
			self.application.duck.selfDrive()
			# If the user selects to contol the duck manualy
		elif (message=='Manual'):
			Utilities.log("Manual Contol")
			self.application.duck.drive = False
			self.application.duck.stop()
			#If the user wants to save the frames of the camera
		# If the user presses shutdown
		elif (message == "shutdown"):
			DrivingDuck.shutdown()
		#Error Catching
		else:
			Utilities.log("An unnexpected error cooured, from:" + message)