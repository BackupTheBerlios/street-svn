#The Core of CodeWorld.  Handles all incoming network traffic.
#Additionally, Core coordinates between the different CWModules.

import exceptions
import string
import sys

from select import select

from CWModules import Events, Network
from CWModules.Server import LoginServer

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
