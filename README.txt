COUNTDOWN! Networked shell edition.
---------------------------------------
Written by Adam Beagle

This edition can only be played on 2 different machines via network. 
Earlier versions that were playable on a single machine are not currently available on Github.

SETUP:
Only verified to work with Python 2.7.3, though I don't know of anything that would break compatibility in 3.x.
All included files, excluding CountdownClient.py, must be on the host machine.
CountdownClient.py is the only file needed on the client machine (assuming Python is installed).


To Play:
  HOST: 
	If you'd like to specify a round time, this can be done via command line arguments like so:
		python Countdown_shell_network.py /t ###
	Where ## is the round time (as an integer) you would like. This can be any number 3 digits or fewer.

	Otherwise, Countdown_shell_network.py can be run with no arguments to use the default round time.

	Please note that running in anything but a Windows shell (e.g. in a Python IDE) results in some text formatting problems.
  

  CLIENT:
	Must specify host IP on command line. Port is optional. Usage is:
		python CountdownClient.py /h host_ip:port
		
		Example: python CountdownClient.py /h 192.168.0.1:23455
	
	If host's IP is not specified at all, the program will not run.
	If port is not specified, the program will default to port 1060 (this is also the default in the server program).
