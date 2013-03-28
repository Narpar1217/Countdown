"""
Copyright (C) 2013 Adam Beagle - All Rights Reserved
You may use, distribute, and modify this code under
the terms of the GNU General Public License,
viewable at http://opensource.org/licenses/GPL-3.0

This copyright notice must be retained with any use
of source code from this file.
"""

import socket
from sys import stderr

################################################################################
class CountdownServer(object):

    #***********************************************************
    # --------------------- CONSTRUCTOR ---------------------- *
    #***********************************************************
    def __init__(self, host='', port=1060, printStatus=True):
        self._prefix = '<&'
        self._postfix = '>'
        self._endStr = 'END'
        self._countStr = 'COUNT'
        self._doCountStr = 'COUNTDOWN'

        if not host:
            host = socket.gethostbyname(socket.gethostname())

        self._printStatus = printStatus

        self._lSock = self._init_lSock(host, port)
        self._cSock = None

    #***********************************************************
    # --------------------- PUBLIC METHODS ------------------- *
    #***********************************************************
    def Close(self):
        if self._printStatus:
            print 'Closing connections.'

        self.Send('', self._endStr)
        self._cSock.close()
        self._lSock.close()

    #-----------------------------------------------------------
    def Receive(self):
        return self._cSock.recv(1024)

    #-----------------------------------------------------------
    def Send(self, msg, mType):
        toSend = '{0}{1}{2}{3}'.format(self._prefix,
                                       str(mType),
                                       self._postfix, msg)
        
        self._cSock.sendall(toSend)

    #-----------------------------------------------------------
    def SendCountLen(self, countLen):
        self.Send(str(countLen), self._countStr)

    #-----------------------------------------------------------
    def SendStartCount(self):
        self.Send('', self._doCountStr)

    #-----------------------------------------------------------
    def Start(self):
        self._lSock.listen(1)

        if self._printStatus:
            print 'Listening on', self._lSock.getsockname(), '\n'

        self._cSock, sockname = self._lSock.accept()

        if self._printStatus:
            print 'Connected to', sockname, '\n\n'


    #***********************************************************
    # -------------------- PRIVATE METHODS ------------------- *
    #***********************************************************
    def _init_lSock(self, host, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))

        return s

    #***********************************************************
    # ----------------------- PROPERTIES --------------------- *
    #***********************************************************



