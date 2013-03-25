COUNTDOWN! Networked shell edition.
---------------------------------------
Written by Adam Beagle


SETUP:
All included files, excluding CountdownClient.py, must be on the host machine.
CountdownClient.py is the only file needed on the client machine (assuming Python is installed).


To Play:
  HOST: 
	If you'd like to specify a round time, this can be done via command line arguments like so:
		python Countdown_shell_network.py /t ###
	Where ## is the round time (as an integer) you would like. This can be any number 3 digits or fewer.

	Otherwise, you can just run Countdown_shell_network.py to use the default round time.

	Please note that running in anything but a Windows shell (e.g. in a Python IDE) results in some text formatting problems.
  
  CLIENT:
	Must specify host on command line. Usage is:
		python CountdownClient.py /h host_ip:port
		
		Example: python CountClient.py /h 192.168.0.1:23455
	
	If host's IP is not specified at all, the program cannot be run.
	If port is not specified, the program will default to port 1060 (this is also the default in the server program).