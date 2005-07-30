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


#Base module for a User, maintains both a stream and datagram socket.
#Subclass to add functionality for the server and client
import string

from StreetModules import Events, Network

class User:
    def __init__(self, tcp, udp):
        self.tcp = tcp
        self.tcp.handleInput = self.handleInputTCP
        self.tcp.handleOutput = self.handleOutputTCP
        self.tcp.close = self.closeAll
        
        self.udp = udp
        self.udp.handleInput = self.handleInputUDP
        self.udp.handleOutput = self.handleOutputUDP
        self.udp.close = self.closeAll
        
        self.name = ''
        self.pwd = ''   #Not stored by server for security reasons.
        self.isNewUser = False
        self.isGuest = False
        self.address = tcp.getpeername()

    def handleInputTCP(self):
        line = self.tcp.readline()
        if(not line):
            return
        line = line[:-1]
        line = string.split(line, maxsplit = 1)
        command = 'net ' + line[0]
        if(len(line) > 1):
            Events.do(command, self, line[1])
        else:
            Events.do(command, self)

    def handleOutputTCP(self):
        self.tcp.flush()

    def handleInputUDP(self):
        packet = self.udp.read()
        if(not packet):
            return
        line = string.split(packet, maxsplit = 1)
        command = 'net ' + line[0]
        if(len(line) > 1):
            Events.do(command, self, line[1])
        else:
            Events.do(command, self)

    def handleOutputUDP(self):
        pass

    def closeAll(self):
        Events.do('net logout', self)
        Network.TCPSocket.close(self.tcp)
        Network.UDPSocket.close(self.udp)

def bindUDP(user, port):
    print "Binding UDP socket to port %i" % int(port)
    user.udp.connect((user.address[0], int(port)))

