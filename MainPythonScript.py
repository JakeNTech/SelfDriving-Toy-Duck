#Main Script
#Command to run "sudo python3 MainPythonScript.py"
#Command to train "sudo python3 MainPythonScript.py train"
#--------------------
from Scripts import WebInterface, DrivingDuck, Utilites
#This gets all the various scripts that are needed to drive the duck
#This is the script that ties is all togeter
from pygame import mixer
#--------Main Function--------------
if(__name__ == "__main__"):
	arguments = Utilites.get_arguments()
	# This gets the arguments from the Utilities script
	#print(arguments)
	parameters = Utilites.get_parameters(arguments.train)
	#Featches the perameaters
	#print(parameters)
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
