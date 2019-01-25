#Main Script
#Command to run "sudo python3 MainPythonScript.py"
#Command to train "sudo python3 MainPythonScript.py train"
#--------------------
from Scripts import Utilities , WebInterface, DrivingDuck
#This gets all the various scripts that are needed to drive the duck
#This is the script that ties is all togeter

if(__name__ == "__main__"):
	print("Starting")
	arguments = Utilities.get_arguments()
	print("Got Arguments")
	# This gets the arguments from the Utilities script
	#print(arguments)
	parameters = Utilities.get_parameters(arguments.train)
	#Featches the perameaters
	print("Got parameters")
	#print(parameters)
	duck = DrivingDuck.DrivingDuck(parameters)
	# This gets the duck ready for ation
	print("Duck is ready!")
	
	duck.WebInterface = WebInterface.LocalServer(parameters['webserver_parameters'], duck)
	# This starts to host the GUI
	print("Starting GUI")

	print('Quack! Ready to get the bread!')
	duck.WebInterface.stream()
	# Print ready to the shell and then trigger the starting mechanism