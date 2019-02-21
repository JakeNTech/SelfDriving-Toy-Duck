#Main Script
#Command to run "sudo python3 MainPythonScript.py"
#Command to train "sudo python3 MainPythonScript.py train"
#--------------------
from Scripts import Utilities , WebInterface, DrivingDuck
#This gets all the various scripts that are needed to drive the duck
#This is the script that ties is all togeter
from pygame import mixer
import time
#-----------------------
#This is for the realistic duck noises
#---------Sound Playback-------------
def DuckSound(SoundTitle):
	#From https://stackoverflow.com/questions/20021457/playing-mp3-song-on-python
	mixer.init()
	mixer.music.load(SoundTitle)
	mixer.music.play()
#--------Main Function--------------
if(__name__ == "__main__"):
	arguments = Utilities.get_arguments()
	# This gets the arguments from the Utilities script
	#print(arguments)
	parameters = Utilities.get_parameters(arguments.train)
	#Featches the perameaters
	#print(parameters)
	duck = DrivingDuck.DrivingDuck(parameters)
	# This gets the duck ready for ation
	duck.WebInterface = WebInterface.LocalServer(parameters['webserverParameters'],duck)
	print('Quack! Ready to get the bread!')
	duck.WebInterface.stream()
	# Print ready to the shell and then trigger the starting mechanism
	#while True:
	#	sound_Title = "./pissed_off_duck-Mike_Koenig-1752213564.mp3"
		#From http://soundbible.com/1859-Pissed-Off-Duck.html
	#	DuckSound(sound_Title)
	#The above calls the sound playback function to add in the realistic duck noises
	if (str(input("Press 1 to exit"))=="exit"):
		DrivingDuck.Shutdown()
