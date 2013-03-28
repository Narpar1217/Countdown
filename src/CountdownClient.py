"""
CountdownClient.py - Runs an instance of a Countdown client program.

ToDo:
  *An abstracted class for a more generic Client object could be very useful to other projects.


Copyright (C) 2013 Adam Beagle - All Rights Reserved
You may use, distribute, and modify this code under
the terms of the GNU General Public License,
viewable at http://opensource.org/licenses/GPL-3.0

This copyright notice must be retained with any use
of source code from this file.
"""

import socket
from sys import argv, exit, stderr, stdout
from time import sleep

################################################################################
class CountdownClient(object):
    """
    The client program for a Countdown game.
    This should be the only file (assuming a Python installation is present)
    needed on a client machine to run the game.
    """

    #***********************************************************
    # --------------------- CONSTRUCTOR ---------------------- *
    #***********************************************************
    def __init__(self, host, port, printStatus = True):
        self._host = host
        self._port = int(port)
        self._printStatus = printStatus
        self._prefix = '<&'
        self._postfix = '>'
        self._endStr = 'END'
        self._countStr = 'COUNT'
        self._startCountStr = 'COUNTDOWN'
        self._countLen = -1
        self._name = raw_input('\nEnter name: ').title()

        self._sock = self._init_sock()

    #***********************************************************
    # --------------------- PUBLIC METHODS ------------------- *
    #***********************************************************
    def Close(self):
        if self._printStatus:
            print '\nClosing connection...'
        self._sock.shutdown(socket.SHUT_RDWR)
        self._sock.close()

    #------------------------------------------------------------------------
    def Start(self):
        pr = self._printStatus
        s = self._sock
        end = False
        prefix = self._prefix
        postfix = self._postfix
        
        if pr:
            print 'Looking for host...'
        s.connect((self._host, self._port))
        if pr:
           print 'Conected successfully to ' + str(s.getsockname()) + '!\n\n'

        s.sendall(self._name)

        while not end:
            fullMsg = s.recv(1024)

            split = fullMsg.split(prefix)

            for msg in [x for x in split if x]:
                header = msg[:msg.index(postfix)]
                
                try:
                    sendMsg = msg[msg.index(postfix) + 1:]
                except IndexError:
                    sendMsg = ''
                end = self._parse_msg(header, sendMsg, s)

        self.Close()


    #***********************************************************
    # -------------------- PRIVATE METHODS ------------------- *
    #***********************************************************
    def _init_sock(self):
        return socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #-------------------------------------------------------------
    def _parse_msg(self, header, msg, sock):
        end = False
        
        if header[0] == '1':
            print msg
        elif header[0] == '2':
            response = raw_input(msg)
            sock.sendall(response)
        elif header == 'COUNT':
            try:
                self._countLen = int(msg)
            except ValueError:
                print >>stderr, 'Error: Problem with count length value received from server. Program ending.'
                exit(1)
        elif header == 'COUNTDOWN':
            if self._countLen < 0:
                print >>stderr, 'WARNING: countLen not yet defined.'
            self._print_countdown(self._countLen)
        elif header == 'END':
            end = True
        
        return end

    #-------------------------------------------------------------------------
    def _print_countdown(self, secs):
        while secs >= 0:
            stdout.write('%02d\r' % secs)
            stdout.flush()
            secs -= 1
            sleep(1)
            stdout.write('  \r')

##############################################################################
def check_ip(ip):
    valid = True

    ip = ip.split(':')

    if len(ip) == 2:
        ip, port = ip
    elif not len(ip) == 1:
        valid = False
    else:
        ip = ip[0]
        port = None

    if ip.count('.') == 3 and valid:
        try:
            for n in ip.split('.'):
                    if not 0 <= int(n) <= 255:
                        valid = False
                        break
            if port:
                port = int(port)
        except (ValueError, TypeError):
            valid = False

    else:
        valid = False

    return valid

#---------------------------------------------------
def parse_argv(args):
    host = None
    port = None
    
    if '/h' in args:
        try:
            host = args[args.index('/h') + 1]
            if not check_ip(host):
                exit('Invalid IP entered.')

            host = host.split(':')
            if len(host) == 2:
                host, port = host
            elif not len(host) == 1:
                exit('Invalid IP/port entered.')
            else:
                host = host[0]
            
        except IndexError:
            host = None

    if not port:
        port = 1060 #FIXME?: hardcoded default port

    return host, port
            
################################################################################            
if __name__ == '__main__':
    host, port = parse_argv(argv)
    if not host:
        print >>stderr, 'No host entered. Usage: python CountdownClient.py /h ip:port'
        raw_input()
    else:
        c = CountdownClient(host, port)
        c.Start()
