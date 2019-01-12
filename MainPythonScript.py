from Scripts import Utilitys, WebInterface, DrivingDuck
#This gets all the various scripts that are needed to drive the duck
#This is the script that ties is all togeter
if(__name__ == "__main__"):
	args = Utilitys.get_args()
	# This gets the arguments from the Utilitys script

	perms = Utilitys.get_perms(args.train)
	#Featches the perameaters

	duck = SelfDrivingDuck.SelfDrivingDuck(perms)
	# This gets the duck ready for ation

	duck.webinterface = WebInterface.LocalServer(perms['webserver_params'], duck)
	# This starts to host the GUI

	print('Quack! Ready to get the bread!')
	duck.webinterface.stream()
	# Print ready to the shell and then trigger the starting mechanism