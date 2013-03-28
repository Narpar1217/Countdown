###################################################################
                             COUNTDOWN! 
                      Networked shell edition

 "It's more or less like regular Countdown, but played in a shell"
###################################################################
Written by Adam Beagle

********************
* ~ GENERAL INFO ~ *
********************

A game similar to the game show Countdown that is played in a shell. 
Two players can play over LAN.


*******************
* ~~~~ SETUP ~~~~ *
*******************

Python is required to play. The game is only verified to work with Python 2.7.3, but I don't know of anything that would break compatibility in 3.x.
All included files, excluding CountdownClient.py, must be on the host machine.
CountdownClient.py is the only file needed on the client machine (assuming Python is installed).


********************
* ~~ HOW TO USE ~~ *
********************

  HOST: 
	Start the game by running Countdown_shell_network.py.
	Running with no arguments will use the default round time of 30 seconds.

	If you'd like to specify a round time, this can be done via a command line argument like so:
		python Countdown_shell_network.py /t ###
	Where ### is the round time in seconds to use. This can be any integer 3 digits or fewer.
  

  CLIENT:
	
	Start the game by running CountdownClient.py.
	The host's IP address must be specified. Port is optional. Usage is:
		python CountdownClient.py /h host_ip:port
		
		Example: python CountdownClient.py /h 192.168.0.1:23455
	
	If host's IP is not specified at all, the program will not run.
	If port is not specified, the program will default to port 1060 (this is also the default in the server program).
