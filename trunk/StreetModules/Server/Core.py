#Copyright (C) 2004-2005 Randall Leeds
#
#This file is part of The Street.
#
#The Street is free software; you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation; either version 2 of the License, or
#(at your option) any later version.
#
#The Street is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with The Street; if not, write to the Free Software
#Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301

#The Core of The Street.  Handles all incoming network traffic.
#Additionally, Core coordinates between the different StreetModules.

import exceptions
import string
import sys

from select import select

from StreetModules import Events, Network
from StreetModules.Server import LoginServer

userNames = {}

def run():
    while running:
        r, w, e = Network.multiplex(1)
        for sock in r:
            try:
                sock.handleInput()
            except Exception, exc:
                if(exc.__class__ != 'socket.error'):
                    print "Unhandled exception:", exc
        for sock in w:
            sock.handleOutput()
        for sock in e:
            sock.close()
    server.close()

def init():
    global running, server
    server = LoginServer.LoginServer()
    server.bind(('', 4242))
    server.listen(5)
    running = True

def quit():
    global running
    running = False
