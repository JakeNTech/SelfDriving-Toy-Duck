#Main Script
#Command to run "sudo python3 MainPythonScript.py"
#Command to train "sudo python3 MainPythonScript.py train"
#--------------------
from Scripts import Utilities , WebInterface, DrivingDuck
#This gets all the various scripts that are needed to drive the duck
#This is the script that ties is all togeter
from pygame import mixer
#-----------------------
#This is for the realistic duck noises
#---------Sound Playback-------------
def DuckSound(SoundTitle):
	#From https://stackoverflow.com/questions/20021457/playing-mp3-song-on-python
	mixer.init()
	mixer.music.load(SoundTitle)
	mixer.music.play()
#Settigns and configurations
parameters = {
	"duckParameters": {
		'width': 320,
		'height': 240,
		'pigame': "False",
		'verbose': "True",
		'channels': 3,
		'duckConfiguration': {
			"FORWARD": {"pin":13,"lable_code":0},
			"RIGHT": {"pin":11, "lable_code":1},
			"LEFT": {"pin":18, "lable_code":2},
			"BACKWARDS": {"pin":15, "lable_code":-1},
			"SPEED":{"pin": 16, "default":55}
		}
	}
	,'cameraParameters':{
		'width': 320,
		'height': 240
	}
	,'webserverParameters':{
		'duck': None
	}
	"headParameters":{
	"model":"PathToFile"
	}
}
#--------Main Function--------------
if(__name__ == "__main__"):
	parameters = parameters
	#The line above runs the perameters function
	duck = DrivingDuck.DrivingDuck(parameters)
	# This gets the duck ready for ationxt
	duck.WebInterface = WebInterface.LocalServer(parameters['webserverParameters'],duck)
	# This starts to host the GUI
	print('Quack! Ready to get the bread!')
	duck.WebInterface.stream()
	# Print ready to the shell and then trigger the starting mechanism

	#while True:
	#	sound_Title = "./pissed_off_duck-Mike_Koenig-1752213564.mp3"
		#From http://soundbible.com/1859-Pissed-Off-Duck.html
	#	DuckSound(sound_Title)
	#The above calls the sound playback function to add in the realistic duck noises
