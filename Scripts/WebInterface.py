
#--------------------
# Imports the camerefeed from the DuckCamera script
from Scripts import Utilities
from Scripts.DuckCamera import CameraFeed
from Scripts import DrivingDuck
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

class LocalServer(tornado.web.Application):
	#Class to help contain the code
	def __init__(self,parameters,_duck):
		Utilities .log("Init. Server",1)
		#logs the session start
		self.duck= _duck
		self.camera = self.duck.camera.picam
		self.port = parameters['port']

		root = Utilities.root_accsess()
		path = os.path.join(root, '../../SelfDriving-Toy-Duck')
		#Get root privlages on pi and then adjust paths to find the right files

		self.handlers = [(r"/", IndexHandler),(r"/websocket",WebSocket),(r'/static/(.*)', tornado.web.StaticFileHandler, {'path':path})]
	def stream(self):
		settings = {'debug':True}
		super(LocalServer,self).__init__(self.handlers, **settings)
		CameraFeed(self.duck)
		self.listen(self.port)
		tornado.ioloop.IOLoop.instance().start()
		#This starts the camera stream for the duck, and users a pre-defined loop
class IndexHandler(tornado.web.RequestHandler):
	def get(self):
		self.render("../WebServer/index.html", port=self.application.port, mode=self.application.duck.trainMode)

class ErrorHandler(tornado.web.RequestHandler):
	def get(self):
		self.send_error(status_code=403)

class WebSocket(tornado.websocket.WebSocketHandler):
	def loop(self):
		try:
			self.write_message(base64.b64encode(self.application.duck.camera.last_img_bytes))
		except tornado.websocket.WebSocketClosedError:
			self.camera_loop.stop()
	def on_message(self, message):
		#This starts an infinate loop when its called up
		if message == "readCamera":
			self.cameraLoop = PeriodicCallback(self.loop, 150)
			self.cameraLoop.start()
			#This sets the camera to 15 Frames per second
			# It also makes a loop that will keep the camera stream alive
		elif message =="About":
			RequestHandler.redirect("../WebServer/AboutPage/about.html")
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
		elif (message=='saveFrames'):
			Utilities.log("Saving frames")
			self.application.duck.traindata.save()
			self.application.duck.drive = False
		# If the user presses shutdown
		elif (message=="Shutdown"):
			DrivingDuck.shutdown()
		#Error Catching
		else:
			Utilities.log("An unnexpected error cooured, from:" + message)
