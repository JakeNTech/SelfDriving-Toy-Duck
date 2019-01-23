#Main Script
#--------------------
from Scripts import Utilitys, WebInterface, DrivingDuck
#This gets all the various scripts that are needed to drive the duck
#This is the script that ties is all togeter

if(__name__ == "__main__"):
	arguments = Utilitys.get_arguments()
	# This gets the arguments from the Utilitys script

	parameters = Utilitys.get_parameters(arguments.train)
	#Featches the perameaters

	duck = DrivingDuck.DrivingDuck(parameters)
	# This gets the duck ready for ation

	duck.webinterface = WebInterface.LocalServer(parameters['webserver_params'], duck)
	# This starts to host the GUI

	print('Quack! Ready to get the bread!')
	duck.webinterface.stream()
	# Print ready to the shell and then trigger the starting mechanism