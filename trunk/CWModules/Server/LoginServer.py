#A simple TCPSocket that handles new connections
import dbhash
import sha
import string

from CWModules.Network import TCPSocket, UDPSocket
from CWModules.User import User

userNames = {}
pwdDB = dbhash.open('CWData/Server/pwd.db', 'c')

class LoginServer(TCPSocket):
    def __init__(self):
        TCPSocket.__init__(self)

    def handleInput(self):
        newUser = User(TCPSocket(self.accept()[0]), UDPSocket())
        newUser.tcp.write('bindUDP %i\n' % newUser.udp.getsockname()[1])
        newUser.tcp.write('login user\n')

def login(user, command = ''):
    #Already logged in?
    if(user.name and user.name in userNames):
        return
    
    line = string.split(command, maxsplit = 1)
    if(line[0] == 'user'):
        if(len(line) == 2):
            user.name = line[1]
            user.tcp.write('login pass\n')
    elif(line[0] == 'pass'):
        if(not user.name or user.name not in pwdDB or len(line) != 2):
            user.tcp.write('login badpass\n')
            return
        pwdSHA = sha.new(line[1])
        if(pwdDB[user.name] == 'new' or pwdDB[user.name] == pwdSHA.digest()):
            user.tcp.write('login ok\n')
            print "%s logged in." % user.address[0]
            if(pwdDB[user.name] == 'new'):
                pwdDB[user.name] = pwdSHA.digest()
            userNames[user.name] = user
        else:
            user.tcp.write('login badpass\n')
    elif(line[0] == 'newuser'):
        if(len(line) == 2):
            user.name = line[1]
            if(user.name in pwdDB):
                user.tcp.write('login userdup\n')
                user.name = ''
                return
            pwdDB[user.name] = 'new'
            user.tcp.write('login pass\n')
            user.isNewUser = True
        
def logout(user):
    if(user.name in userNames):
        print "%s logged out." % user.address[0]
        del userNames[user.name]
