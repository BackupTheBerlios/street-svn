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

#A simple TCPSocket that handles new connections
import dbhash
import sha

from StreetModules.Network import TCPSocket, UDPSocket
import Core
from StreetModules.User import User

pwdDB = dbhash.open('StreetData/Server/pwd.db', 'c')

class LoginServer(TCPSocket):
    def __init__(self):
        TCPSocket.__init__(self)

    def handleInput(self):
        newUser = User(TCPSocket(self.accept()[0]), UDPSocket())
        newUser.tcp.write('bindUDP %i\n' % newUser.udp.getsockname()[1])
        newUser.tcp.write('login user\n')

def login(user, command = ''):
    line = command.split(' ', 1)
    if(line[0] == 'user'):
        if(len(line) == 2):
            user.name = line[1]
            user.tcp.write('login pass\n')
    elif(line[0] == 'pass'):
        if(user.name and user.name in Core.userNames):
            user.tcp.write('login duplicate\n')
            return
        if(not user.name or user.name not in pwdDB or len(line) != 2):
            user.tcp.write('login badpass\n')
            return
        pwdSHA = sha.new(line[1])
        if(pwdDB[user.name] == 'new' or pwdDB[user.name] == pwdSHA.digest()):
            user.tcp.write('login ok\n')
            print "%s logged in from %s." % (user.name, user.address[0])
            if(pwdDB[user.name] == 'new'):
                pwdDB[user.name] = pwdSHA.digest()
            Core.userNames[user.name] = user
        else:
            user.tcp.write('login badpass\n')
    elif(line[0] == 'newuser'):
        if(len(line) == 2):
            user.name = line[1]
            if(user.name in pwdDB):
                user.tcp.write('login taken\n')
                user.name = ''
                return
            pwdDB[user.name] = 'new'
            user.tcp.write('login pass\n')
            user.isNewUser = True
    elif(line[0] == 'guest'):
        user.tcp.write('login ok\n')
        if(len(line) == 2):
            suffix = 0
            while(line[1] + str(suffix) in Core.userNames or line[1] + str(suffix) in pwdDB):
                suffix += 1
            user.name = line[1] + str(suffix)
            print "%s logged in as a guest from %s." % (user.name, user.address[0])
            Core.userNames[user.name] = user
        
def logout(user):
    if(user.name in Core.userNames):
        print "%s logged out." % user.name
        del Core.userNames[user.name]
